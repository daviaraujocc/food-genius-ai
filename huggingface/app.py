import gradio as gr
from typing import Tuple, Dict
import torch
from PIL import Image as PILImage

from model_builder import create_effnetb2_model
from timeit import default_timer as timer


with open('class_names.txt', 'r') as file:
    class_names = file.read().splitlines()


food_nonfood_class_names = ['food', 'non_food']


effnetb2_food101, effnetb2_food101_transforms = create_effnetb2_model(num_classes=len(class_names))
effnetb2_food101.load_state_dict(torch.load(f='pretrained_effnetb2_food_101.pth', map_location='cpu'))

effnetb2_model_food_nonfood, effnetb2_food_nonfood_transforms= create_effnetb2_model(num_classes=len(food_nonfood_class_names))
effnetb2_model_food_nonfood.load_state_dict(torch.load(f='pretrained_effnetb2_food_or_nonfood.pth', map_location='cpu'))

def predict(img) -> Tuple[Dict, float]:
    """Transforms and performs a prediction on img and returns prediction and time taken."""
    # Start the timer
    start_time = timer()
    
    # Transform the image for the food vs. nonfood model
    img_transformed = effnetb2_food_nonfood_transforms(img).unsqueeze(0).to('cpu')
    
    # Perform food vs. nonfood classification
    effnetb2_model_food_nonfood.eval()
    with torch.inference_mode():
        food_nonfood_pred_probs = torch.softmax(effnetb2_model_food_nonfood(img_transformed), dim=1)
    
    # Check if the image is classified as food
    is_food = food_nonfood_pred_probs[0][0] > 0.5  # Assuming threshold of 0.5 for food
    
    if is_food:
        img_transformed = effnetb2_food101_transforms(img).unsqueeze(0).to('cpu')
        
        effnetb2_food101.eval()
        with torch.inference_mode():
            pred_probs = torch.softmax(effnetb2_food101(img_transformed), dim=1)
        
        pred_labels_and_probs = {class_names[i]: float(pred_probs[0][i]) for i in range(len(class_names))}
    else:
        pred_labels_and_probs = {'nonfood': float(food_nonfood_pred_probs[0][1])}
    
    pred_time = round(timer() - start_time, 5)
    
    return pred_labels_and_probs, pred_time


def classify(img: PILImage.Image) -> Tuple[Dict, float]:
    predictions, time_taken = predict(img)
    if 'nonfood' in predictions:
        return gr.update(value="This is not food. Please try again with a food image.", visible=True), time_taken
    return predictions, time_taken

title = "FoodGeniusAI"
description = """
FoodGeniusAI is an AI-powered application built using the EfficientNetB2 model. It can detect the type of food in an image and determine whether the image contains food or not. 
Please note that the photo needs to be close to the food for accurate detection; otherwise, it may not work correctly.

**Author:** Davi Araujo (@daviaraujocc)
"""
article = "Created using EfficientNetB2 model"


app = gr.Interface(fn=classify,
                   inputs=gr.Image(type="pil"),
                   outputs=[gr.Label(num_top_classes=3, label="Predictions"), gr.Number(label="Prediction Time")],
                   title=title,
                   description=description,
                   article=article,
                   examples=[["examples/pizza.jpg"], ["examples/steak.jpg"], ["examples/sushi.jpg"], ["examples/ramen.jpg"]]
                   )

app.launch(share=False)