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
from timeit import default_timer as timer
import csv

def save_and_plot_results(results, model_name, model_path):
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    
    results_path = os.path.join(model_path, f"{model_name}_results.csv")
    results_list = [
        {
            "epoch": epoch + 1,
            "train_loss": results["train_loss"][epoch],
            "train_acc": results["train_acc"][epoch],
            "test_loss": results["test_loss"][epoch],
            "test_acc": results["test_acc"][epoch]
        }
        for epoch in range(len(results["train_loss"]))
    ]
    
    with open(results_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["epoch", "train_loss", "train_acc", "test_loss", "test_acc"])
        writer.writeheader()
        writer.writerows(results_list)
    
    epochs = range(len(results["train_loss"]))
    plt.figure(figsize=(14, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(epochs, results["train_loss"], label="Train Loss")
    plt.plot(epochs, results["test_loss"], label="Test Loss")
    plt.title("Training and Testing Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(epochs, results["train_acc"], label="Train Accuracy")
    plt.plot(epochs, results["test_acc"], label="Test Accuracy")
    plt.title("Training and Testing Accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
    
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{model_name}_results_{current_time}.png"
    plt.savefig(os.path.join(model_path, filename))
    print(f"Results saved to {model_path}")
    plt.close()

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

def train_food_or_nonfood(epochs, model_path, model_name, device, batch_size, split_size, lr):
    data_dir = Path("data")
    train_dir = data_dir / "food5k" /  "training"
    test_dir = data_dir / "food5k" / "validation"

    effnetb2_5k_food_or_nonfood, effnetb2_transforms = model_builder.create_effnetb2_model(num_classes=2)
    food_5k_transforms = transforms.Compose([
        transforms.TrivialAugmentWide(), effnetb2_transforms,
    ])

    train_dataloader_food5k, test_dataloader_food5k, class_names = data_setup.create_dataloaders_from_dir(train_dir, test_dir, food_5k_transforms, batch_size, 2, split_size)

    optimizer = torch.optim.Adam(effnetb2_5k_food_or_nonfood.parameters(), lr=lr)
    loss_fn = torch.nn.CrossEntropyLoss(label_smoothing=0.1)
    
    start_time = timer()
    effnetb2_5k_nonfood_results = engine.train(
        model=effnetb2_5k_food_or_nonfood.to(device),
        train_dataloader=train_dataloader_food5k,
        test_dataloader=test_dataloader_food5k,
        optimizer=optimizer,
        loss_fn=loss_fn,
        epochs=epochs,
        device=device
    )
    end_time = timer()
    training_time = end_time - start_time
    print(f"Training time for {model_name}: {training_time:.2f} seconds")

    model_path = os.path.join(model_path, os.path.splitext(model_name)[0])

    utils.save_model(model=effnetb2_5k_food_or_nonfood, target_dir=model_path, model_name=model_name)
    save_and_plot_results(effnetb2_5k_nonfood_results, model_name, model_path)

def train_food101(epochs, model_path, model_name, device, batch_size, split_size, lr):
    data_dir = Path("data")

    effnetb2_101, effnetb2_transforms = model_builder.create_effnetb2_model(num_classes=101)
    food_101_transforms = transforms.Compose([
        transforms.TrivialAugmentWide(), effnetb2_transforms,
    ])


    train_set = datasets.Food101(root=data_dir, split="train", transform=food_101_transforms, download=True)
    val_set = datasets.Food101(root=data_dir, split="test", transform=food_101_transforms, download=True)

    train_dataloader_food101, test_dataloader_food101, class_names = data_setup.create_dataloaders_from_dataset(train_set, val_set, batch_size, 2, split_size=split_size)
    
    optimizer = torch.optim.Adam(effnetb2_101.parameters(), lr=lr)
    loss_fn = torch.nn.CrossEntropyLoss(label_smoothing=0.1)

    start_time = timer()
    effnetb2_101_results = engine.train(
        model=effnetb2_101.to(device),
        train_dataloader=train_dataloader_food101,
        test_dataloader=test_dataloader_food101,
        optimizer=optimizer,
        loss_fn=loss_fn,
        epochs=epochs,
        device=device
    )
    end_time = timer()
    training_time = end_time - start_time
    print(f"Training time for {model_name}: {training_time:.2f} seconds")

    model_path = os.path.join(model_path, os.path.splitext(model_name)[0])

    utils.save_model(model=effnetb2_101, target_dir=model_path, model_name=model_name)
    save_and_plot_results(effnetb2_101_results, model_name, model_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train EfficientNetB2 models")
    parser.add_argument("--model", type=str, choices=["food_or_nonfood", "food101"], required=True, help="Model to train")
    parser.add_argument("--epochs", type=int, default=5, help="Number of epochs to train")
    parser.add_argument("--model_path", type=str, default="results", help="Path to save the trained model")
    parser.add_argument("--model_name", type=str, default="model.pth", help="Name of the saved model")
    parser.add_argument("--device", type=str, choices=["cpu", "cuda"], default="cuda", help="Device to use for training")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for training, higher batch size may require more memory and may not fit on GPU")
    parser.add_argument("--split_size", type=float, default=0.2, help="Fraction of the dataset to use for training, set to less than 1 to use a fraction of the dataset")
    parser.add_argument("--learning_rate", type=float, default=0.001, help="Learning rate for training")

    args = parser.parse_args()

    device = torch.device(args.device)

    if args.model == "food_or_nonfood":
        download_food5k()
        train_food_or_nonfood(args.epochs, args.model_path, args.model_name, device, args.batch_size, args.split_size, args.learning_rate)
    elif args.model == "food101":
        train_food101(args.epochs, args.model_path, args.model_name, device, args.batch_size, args.split_size, args.learning_rate)