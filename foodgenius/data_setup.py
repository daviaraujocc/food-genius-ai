import os
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import foodgenius.utils as utils

NUM_WORKERS = os.cpu_count()

def create_dataloaders_from_dir(
    train_dir: str, 
    test_dir: str, 
    transforms: transforms.Compose, 
    batch_size: int, 
    num_workers: int=NUM_WORKERS,
    split_size: float=1
):

  train_data = datasets.ImageFolder(train_dir, transform=transforms)
  test_data = datasets.ImageFolder(test_dir, transform=transforms)
  class_names = train_data.classes


  if split_size < 1:
    train_data, _ = utils.split_dataset(train_data, split_size)
    test_data, _ = utils.split_dataset(test_data, split_size)


  train_dataloader = DataLoader(
      train_data,
      batch_size=batch_size,
      shuffle=True,
      num_workers=num_workers,
      pin_memory=True,
  )

  test_dataloader = DataLoader(
      test_data,
      batch_size=batch_size,
      shuffle=False,
      num_workers=num_workers,
      pin_memory=True,
  )

  return train_dataloader, test_dataloader, class_names

def create_dataloaders_from_dataset(
    train_data: datasets, 
    test_data: datasets, 
    batch_size: int, 
    num_workers: int=NUM_WORKERS,
    split_size: float=1
):

  class_names = train_data.classes

  if split_size < 1:
    train_data, _ = utils.split_dataset(train_data, split_size)
    test_data, _ = utils.split_dataset(test_data, split_size)


  train_dataloader = DataLoader(
      train_data,
      batch_size=batch_size,
      shuffle=True,
      num_workers=num_workers,
      pin_memory=True,
  )

  test_dataloader = DataLoader(
      test_data,
      batch_size=batch_size,
      shuffle=False,
      num_workers=num_workers,
      pin_memory=True,
  )

  return train_dataloader, test_dataloader, class_names

