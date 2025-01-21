<div align="center">
    <h1 align="center">Food Genius AI</h1>
    <br>
    <strong>A powerful AI application built using EfficientNetB2 that can detect the type of food in an image and determine whether the image contains food or not.<br></strong>
    <i>Powered by BentoML 🍱 and PyTorch 🔥</i>
    <br>
</div>
<br>

<div align="center">
    <a href="README.md">🇺🇸 English</a> | <a href="README.pt-br.md">🇧🇷 Português (Brasil)</a>
</div>
<br>

## 📖 Introduction 📖
FoodGeniusAI is an AI-powered application that uses EfficientNetB2 to classify food images. It can identify the type of food and determine if the image contains food.

<div align="center">
    <img src="https://github.com/daviaraujocc/food-genius-ai/blob/main/assets/images/demo.gif" alt="demo" >   
</div>

### 📊 Models 📊
FoodGeniusAI uses two main models for classification:

1. **Food or Non-Food Model (Food5K)**
    - This model classifies images as either food or non-food using Food5k dataset.

2. **Food101 Model**
    - This model classifies images into 101 different types of food using the Food101 dataset.

Both models are based on the EfficientNetB2 architecture and were trained using PyTorch. Pretrained models are located in the `models` directory.

## Glossary
- [Requirements](#-requirements-)
- [Running the Service](#-running-the-service-)
- [Using the Service](#-using-the-service-)
- [Hugging Face App](#-hugging-face-app-)
- [Training and Prediction](#-training-and-prediction-)
- [Jupyter Notebooks](#-jupyter-notebooks-)
- [Deploying to Kubernetes](#-deploying-to-kubernetes-)

## 📋 Requirements 📋

- Python 3.11+
- BentoML
- Pip

## 🏃‍♂️ Running the Service 🏃‍♂️
> For GPU use bentofile.gpu.yaml and requirements/gpu-requirements.txt.

1. Clone the repository:
    ```bash
    git clone https://github.com/daviaraujocc/FoodGeniusAI.git
    cd FoodGeniusAI
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements/cpu-requirements.txt
    ```

3. Serve the BentoML service:
    ```bash
    bentoml serve 
    ```

You can then open your browser at http://127.0.0.1:3000 and interact with the service through Swagger UI.


### 🐳 Containers 🐳

To run the service in a container, you can use the following commands:

```bash
bentoml build -f bentofile.yaml
```

> Executing this command will create on your home the directory `bentoml` with the service files.

```bash
bentoml containerize foodgenius-service
```

```bash
docker run -p 3000:3000 foodgenius-service:$(bentoml get foodgenius-service:latest | yq -r ".version")
```



## 🌐 Using the Service 🌐
You can use the BentoML service with HTTP requests. Here are some examples:

### cURL
The following example shows how to send a request to the service to classify an image via cURL:

```bash
curl -X POST \ 
  'http://127.0.0.1:3000/classify' \   
  -H "Content-Type: multipart/form-data" \  
  -F "img=@examples/images/pizza.jpg"
```

## 🤗 Hugging Face App 🤗

You can also try out the FoodGeniusAI application on Hugging Face Spaces:

[FoodGeniusAI on Hugging Face](https://huggingface.co/spaces/daviaraujocc/foodgeniusai)



## 🏋️‍♂️ Training and Prediction 🏋️‍♂️

### Training

You can train the models using the `train.py` script. Here are the steps:

1. Train the `food_or_nonfood` model:
    ```bash
    python train.py --model food_or_nonfood --epochs 10 --model_name pretrained_effnetb2_food_or_nonfood.pth --batch_size 32 --device cpu
    ```

2. Train the `food101` model:
    ```bash
    python train.py --model food101 --epochs 5 --model_name pretrained_effnetb2_food101.pth --split_size 0.2 --batch_size 32 --device cpu
    ```

Results for the training process will be saved in the `results` directory.

### Prediction

You can make predictions using the `predict.py` script. Here are the steps:

1. Predict using the `food_or_nonfood` model:
    ```bash
    python predict.py --model food_or_nonfood --image path/to/image.jpg --model_path models/pretrained_effnetb2_food_or_nonfood.pth --device cpu
    ```

2. Predict using the `food101` model:
    ```bash
    python predict.py --model food101 --image path/to/image.jpg --model_path models/pretrained_effnetb2_food101.pth --class_names_path class_names.txt --device cpu
    ```

## 📓 Jupyter Notebooks 📓

This repository includes several Jupyter Notebooks that demonstrate the training and prediction processes using EfficientNetB2.

Before running the notebooks, install the required dependencies using conda or venv:

```bash
conda env create -f environment.yml
conda activate foodgenius
```

### Training Notebooks

1. **Food or Non-Food Classification**
    - [effnetb2_training_food_or_nonfood.ipynb](effnetb2_training_food_or_nonfood.ipynb)
    - Trains a model on the Food5K dataset to classify images as food or non-food.

2. **Food101 Classification**
    - [effnetb2_training_food101.ipynb](effnetb2_training_food101.ipynb)
    - Trains a model on the Food101 dataset to classify images into 101 types of food.

### Prediction Notebook

1. **EfficientNetB2 Prediction**
    - [effnetb2_predict.ipynb](effnetb2_predict.ipynb)
    - Demonstrates how to use the trained EfficientNetB2 model to make predictions on new images.

## 🚀 Deploying to Kubernetes 🚀

To deploy the service to production, you can use the following commands:

```bash
bentoml build -f bentofile.yaml
```

```bash
bentoml containerize foodgenius-service:latest --image-tag {your-username-repo}/foodgenius-service:latest
```

```bash
docker push {your-username-repo}/foodgenius-service:latest
```

Edit the `manifests/deployment.yaml` file to include your image, then apply it to your Kubernetes cluster:
```bash
kubectl apply -f manifests/deployment.yaml
```

## 📝 Author
**Davi Araujo (@daviaraujocc)**