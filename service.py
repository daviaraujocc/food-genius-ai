import bentoml
from PIL import Image as PILImage, UnidentifiedImageError
import torch
import foodgenius.model_builder as model_builder
from typing import Dict
from timeit import default_timer as timer
from bentoml.exceptions import BadInput
import os


# Load Class Names
with open('class_names.txt', 'r') as file:
    class_names = file.read().splitlines()

food_nonfood_class_names = ['food', 'non_food']


@bentoml.service(name="foodgenius-service", resources={"cpu": "1", "memory": "512Mi"})
class FoodGenius:
    def __init__(self):
        device = os.getenv("BENTOML_DEVICE", "cpu")
        self.device = torch.device(device)


        effnetb2_101_model, effnetb2_101_transforms = model_builder.create_effnetb2_model(num_classes=len(class_names))
        effnetb2_101_model.load_state_dict(torch.load(f='models/pretrained_effnetb2_food_101.pth', map_location='cpu'))

        effnetb2_model_food_nonfood, effnetb2_food_nonfood_transforms = model_builder.create_effnetb2_model(num_classes=len(food_nonfood_class_names))
        effnetb2_model_food_nonfood.load_state_dict(torch.load(f='models/pretrained_effnetb2_food_or_nonfood.pth', map_location='cpu'))

        self.effnetb2_101_model = effnetb2_101_model
        self.effnetb2_101_transforms = effnetb2_101_transforms

        self.effnetb2_model_food_nonfood = effnetb2_model_food_nonfood
        self.effnetb2_food_nonfood_transforms = effnetb2_food_nonfood_transforms

    @bentoml.api
    def classify(self, img: PILImage.Image) -> Dict:
        start_time = timer()

        try:
            # Check if the image format is supported
            if img.format not in ["JPEG", "JPG", "PNG"]:
                return {"error": "Unsupported image format. Please upload a JPG, JPEG, or PNG image."}

            if img.mode == 'RGBA':
                img = img.convert('RGB')

            img_transformed = self.effnetb2_food_nonfood_transforms(img).unsqueeze(0).to(self.device)

            self.effnetb2_model_food_nonfood.eval()
            with torch.inference_mode():
                food_nonfood_pred_probs = torch.softmax(self.effnetb2_model_food_nonfood(img_transformed), dim=1)

            is_food = food_nonfood_pred_probs[0][0] > 0.5  # Assuming threshold of 0.5 for food

            if is_food:
                img_transformed = self.effnetb2_101_transforms(img).unsqueeze(0).to(self.device)

                self.effnetb2_101_model.eval()
                with torch.inference_mode():
                    pred_probs = torch.softmax(self.effnetb2_101_model(img_transformed), dim=1)
                    pred_labels_and_probs = {class_names[i]: float(pred_probs[0][i]) for i in range(len(class_names))}
            else:
                pred_labels_and_probs = {'nonfood': float(food_nonfood_pred_probs[0][1])}

            pred_time = round(timer() - start_time, 5)

            return {"predictions": pred_labels_and_probs, "time_taken": pred_time, "top_prediction": max(pred_labels_and_probs, key=pred_labels_and_probs.get)}

        except BadInput:
            return {"error": "Invalid input. Please upload a valid JPG, JPEG, or PNG image."}
    