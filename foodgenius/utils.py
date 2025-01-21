import torch
import os
from torch.utils.data import random_split
from torchvision import datasets

def save_model(model, target_dir, model_name):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    model_path = os.path.join(target_dir, model_name)
    
    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")

def split_dataset(dataset:datasets,
                  split_size:float=0.2,
                  seed:int=34):
    torch.manual_seed(seed)
    length_1 = int(len(dataset) * split_size)
    length_2 = len(dataset) - length_1


    random_split_1, random_split_2 = random_split(dataset, [length_1, length_2], generator=torch.Generator().manual_seed(seed))

    return random_split_1, random_split_2