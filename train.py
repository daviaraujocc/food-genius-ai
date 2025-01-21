import argparse
import torch
from pathlib import Path
from torchvision import datasets, transforms
import foodgenius.model_builder as model_builder
import foodgenius.engine as engine
import foodgenius.data_setup as data_setup
import foodgenius.utils as utils
import matplotlib.pyplot as plt
import os
import subprocess
from datetime import datetime

def plot_results(results, model_name):
    epochs = range(len(results["train_loss"]))
    plt.figure(figsize=(10, 7))
    plt.plot(epochs, results["train_loss"], label="Train Loss")
    plt.plot(epochs, results["test_loss"], label="Test Loss")
    plt.plot(epochs, results["train_acc"], label="Train Accuracy")
    plt.plot(epochs, results["test_acc"], label="Test Accuracy")
    plt.title(f"Training and Testing Results for {model_name}")
    plt.xlabel("Epochs")
    plt.ylabel("Loss/Accuracy")
    plt.legend()

    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Get current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{model_name}_results_{current_time}.png"
    plt.savefig(os.path.join(results_dir, filename))
    print(f"Results saved to {os.path.join(results_dir, filename)}")


def download_food5k():
    data_dir = Path("data/food5k")
    if data_dir.exists():
        print("Dataset already exists. Skipping download.")
        return
    try:
        subprocess.run(["kaggle", "--version"], check=True, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Kaggle CLI not found. Please install it using `pip install kaggle`.")

    subprocess.run(["kaggle", "datasets", "download", "-d", "trolukovich/food5k-image-dataset", "-p", "data"], check=True)
    subprocess.run(["unzip", "-qo", "data/food5k-image-dataset.zip", "-d", "data/food5k"], check=True)
    print("Dataset downloaded and extracted.")

def train_food_or_nonfood(epochs, model_path, model_name, device, batch_size, split_size):
    data_dir = Path("data")
    train_dir = data_dir / "food5k" /  "training"
    test_dir = data_dir / "food5k" / "validation"

    effnetb2_5k_food_or_nonfood, effnetb2_transforms = model_builder.create_effnetb2_model(num_classes=2)
    food_5k_transforms = transforms.Compose([
        transforms.TrivialAugmentWide(), effnetb2_transforms,
    ])

    train_dataloader_food5k, test_dataloader_food5k, class_names = data_setup.create_dataloaders_from_dir(train_dir, test_dir, food_5k_transforms, batch_size, 2, split_size)

    optimizer = torch.optim.Adam(effnetb2_5k_food_or_nonfood.parameters(), lr=0.001)
    loss_fn = torch.nn.CrossEntropyLoss(label_smoothing=0.1)

    effnetb2_5k_nonfood_results = engine.train(
        model=effnetb2_5k_food_or_nonfood.to(device),
        train_dataloader=train_dataloader_food5k,
        test_dataloader=test_dataloader_food5k,
        optimizer=optimizer,
        loss_fn=loss_fn,
        epochs=epochs,
        device=device
    )

    utils.save_model(model=effnetb2_5k_food_or_nonfood, target_dir=model_path, model_name=model_name)
    plot_results(effnetb2_5k_nonfood_results, model_name)

def train_food101(epochs, model_path, model_name, device, batch_size, split_size):
    data_dir = Path("data")

    effnetb2_101, effnetb2_transforms = model_builder.create_effnetb2_model(num_classes=101)

    train_set = datasets.Food101(root=data_dir, split="train", transform=effnetb2_transforms, download=True)
    val_set = datasets.Food101(root=data_dir, split="test", transform=effnetb2_transforms, download=True)

    train_dataloader_food101, test_dataloader_food101, class_names = data_setup.create_dataloaders_from_dataset(train_set, val_set, batch_size, 2, split_size=split_size)
    
    optimizer = torch.optim.Adam(effnetb2_101.parameters(), lr=0.001)
    loss_fn = torch.nn.CrossEntropyLoss(label_smoothing=0.1)

    effnetb2_101_results = engine.train(
        model=effnetb2_101.to(device),
        train_dataloader=train_dataloader_food101,
        test_dataloader=test_dataloader_food101,
        optimizer=optimizer,
        loss_fn=loss_fn,
        epochs=epochs,
        device=device
    )

    utils.save_model(model=effnetb2_101, target_dir=model_path, model_name=model_name)
    plot_results(effnetb2_101_results, model_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train EfficientNetB2 models")
    parser.add_argument("--model", type=str, choices=["food_or_nonfood", "food101"], required=True, help="Model to train")
    parser.add_argument("--epochs", type=int, default=5, help="Number of epochs to train")
    parser.add_argument("--model_path", type=str, default="models", help="Path to save the trained model")
    parser.add_argument("--model_name", type=str, default="pretrained_effnetb2_feature_extractor.pth", help="Name of the saved model")
    parser.add_argument("--device", type=str, choices=["cpu", "cuda"], default="cuda", help="Device to use for training")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for training, higher batch size may require more memory and may not fit on GPU")
    parser.add_argument("--split_size", type=float, default=1, help="Fraction of the dataset to use for training, set to less than 1 to use a fraction of the dataset")

    args = parser.parse_args()

    device = torch.device(args.device)

    if args.model == "food_or_nonfood":
        download_food5k()
        train_food_or_nonfood(args.epochs, args.model_path, args.model_name, device, args.batch_size, args.split_size)
    elif args.model == "food101":
        train_food101(args.epochs, args.model_path, args.model_name, device, args.batch_size, args.split_size)