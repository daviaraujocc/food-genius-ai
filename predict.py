import argparse
import torch
from PIL import Image
from pathlib import Path
import foodgenius.model_builder as model_builder
import foodgenius.utils as utils

def load_model(model_path, num_classes, device):
    model, transforms = model_builder.create_effnetb2_model(num_classes=num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model, transforms

def predict(image_path, model, transforms, class_names, device):
    img = Image.open(image_path).convert("RGB")
    img_transformed = transforms(img).unsqueeze(0).to(device)

    with torch.inference_mode():
        pred_probs = torch.softmax(model(img_transformed), dim=1)
    
    pred_labels_and_probs = {class_names[i]: float(pred_probs[0][i]) for i in range(len(class_names))}
    top_prediction = max(pred_labels_and_probs, key=pred_labels_and_probs.get)
    
    return pred_labels_and_probs, top_prediction

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict using EfficientNetB2 models")
    parser.add_argument("--model", type=str, choices=["food_or_nonfood", "food101"], required=True, help="Model to use for prediction")
    parser.add_argument("--image", type=str, required=True, help="Path to the image to predict")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the trained model")
    parser.add_argument("--class_names_path", type=str, help="Path to the class names file (required for food101)")
    parser.add_argument("--device", type=str, choices=["cpu", "cuda"], default="cuda", help="Device to use for prediction")

    args = parser.parse_args()

    device = torch.device(args.device)

    if args.model == "food_or_nonfood":
        class_names = ["food", "non_food"]
        num_classes = 2
    elif args.model == "food101":
        if not args.class_names_path:
            raise ValueError("class_names_path is required for food101 model")
        with open(args.class_names_path, 'r') as file:
            class_names = file.read().splitlines()
        num_classes = len(class_names)

    model, transforms = load_model(args.model_path, num_classes, device)
    pred_labels_and_probs, top_prediction = predict(args.image, model, transforms, class_names, device)

    print(f"Predictions: {pred_labels_and_probs}")
    print(f"Top Prediction: {top_prediction}")