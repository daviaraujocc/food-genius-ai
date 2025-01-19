import bentoml
from PIL import Image as PILImage
import torch
import foodgenius.model_builder as model_builder
from typing import Tuple, Dict
from timeit import default_timer as timer

# Load Class Names
with open('class_names.txt', 'r') as file:
    class_names = file.read().splitlines()

food_nonfood_class_names = ['food', 'non_food']


@bentoml.service(name="foodgenius-service", resources={"cpu": "1", "memory": "512Mi"})
class FoodGenius:
    def __init__(self):
        import torch
        effnetb2_model, effnetb2_transforms = model_builder.create_effnetb2_model(num_classes=len(class_names))
        effnetb2_model.load_state_dict(torch.load(f='models/pretrained_effnetb2_food_101.pth', map_location='cpu'))

        food_nonfood_model, food_nonfood_transforms = model_builder.create_effnetb2_model(num_classes=len(food_nonfood_class_names))
        food_nonfood_model.load_state_dict(torch.load(f='models/pretrained_effnetb2_food_or_nonfood.pth', map_location='cpu'))

        self.effnetb2_model = effnetb2_model
        self.effnetb2_transforms = effnetb2_transforms

        self.food_nonfood_model = food_nonfood_model
        self.food_nonfood_transforms = food_nonfood_transforms

    @bentoml.api
    def classify(self, img: PILImage.Image) -> Dict:
    
        start_time = timer()
    
        img_transformed = self.food_nonfood_transforms(img).unsqueeze(0).to('cpu')
    
   
        self.food_nonfood_model.eval()
        with torch.inference_mode():
            food_nonfood_pred_probs = torch.softmax(self.food_nonfood_model(img_transformed), dim=1)
    
        is_food = food_nonfood_pred_probs[0][0] > 0.5  # Assuming threshold of 0.5 for food
    
        if is_food:
            img_transformed = self.effnetb2_transforms(img).unsqueeze(0).to('cpu')
        
            self.effnetb2_model.eval()
            with torch.inference_mode():
                pred_probs = torch.softmax(self.effnetb2_model(img_transformed), dim=1)
                pred_labels_and_probs = {class_names[i]: float(pred_probs[0][i]) for i in range(len(class_names))}
        else:
            pred_labels_and_probs = {'nonfood': float(food_nonfood_pred_probs[0][1])}
    
        pred_time = round(timer() - start_time, 5)
    
        return {"predictions": pred_labels_and_probs, "time_taken": pred_time}
    