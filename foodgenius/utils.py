import torch
import os

def save_model(model, target_dir, model_name):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    model_path = os.path.join(target_dir, model_name)
    
    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")