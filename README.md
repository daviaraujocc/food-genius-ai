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
FoodGeniusAI is an AI-powered food classification system that instantly identifies dishes from images. Built with EfficientNetB2 and BentoML, it offers both food detection and detailed dish classification with 80% accuracy.

<div align="center">
    <img src="https://github.com/daviaraujocc/food-genius-ai/blob/main/assets/images/demo.gif" alt="demo" >   
</div>

### ✨ Key Features

- 🍔 Instant Food Detection: Automatically distinguishes food from non-food images
- 🔍 101 Food Categories: Recognizes a wide variety of dishes with 80% accuracy
- ⚡ Fast Processing: Optimized for real-time classification
- 🚀 Production-Ready: Deployable with BentoML for scalable serving
- 📱 REST API Support: Easy integration with any application

### 📊 Models

FoodGeniusAI uses two EfficientNetB2 models for food classification:

#### 1. Food or Non-Food Detector (Food5K Model)
- **Purpose**: Determines if image contains food
- **Performance**: 90% accuracy
- **Input**: 224x224 RGB images
- **Output**: Binary classification (food/non-food)
- **Training**: Food5K dataset (5,000 images)

#### 2. Food101 Classifier
- **Purpose**: Identifies specific food category
- **Performance**: 80% accuracy
- **Input**: 224x224 RGB images
- **Output**: 101 food categories
- **Training**: Food101 dataset (101,000 images)

#### Classification Pipeline
1. Image → Food/Non-Food Detection
2. If food detected → Food Category Classification
3. Return prediction score for each category

### 🛠️ Core Technologies

- **ML & Training**
  - 🧠 EfficientNetB2: Lightweight and efficient CNN for image classification
  - 🔥 PyTorch: Deep learning framework for model training
  - 📊 Jupyter: Interactive development and model experimentation

- **UI & Serving**
  - 🎨 Gradio: Interactive web interface for model demo
  - 🍱 BentoML: ML model serving and deployment
  - 🐳 Docker: Containerization for consistent deployments

- **Infrastructure**
  - ⚓ Kubernetes: Container orchestration at scale
  - 📈 Prometheus & Grafana: Real-time metrics and visualization

### 🤗 Try it Now! 🤗
Try out FoodGeniusAI instantly on Hugging Face Spaces:

[FoodGeniusAI on Hugging Face](https://huggingface.co/spaces/daviaraujocc/foodgeniusai)


## Glossary
- [Requirements](#-requirements-)
- [Running the Service](#-running-the-service-)
- [Using the Service](#-using-the-service-)
- [Training and Prediction](#-training-and-prediction-)
- [Jupyter Notebooks](#-jupyter-notebooks-)
- [Deploying to Kubernetes](#-deploying-to-kubernetes-)
- [Observability](#-observability-)

## 📋 Requirements 📋

- Python 3.11+
- CUDA-compatible GPU (optional, for faster processing)
- Docker (optional, for containerization)

## 🏃‍♂️ Running the Service 🏃‍♂️

Clone the repository and install the dependencies:
```bash
git clone https://github.com/daviaraujocc/FoodGeniusAI.git
cd FoodGeniusAI
pip install -r requirements/test.txt
```
### Local development

```bash
bentoml serve 
```
> Access at http://127.0.0.1:3000 and interact with the service through the Swagger UI.


### Docker (Recommended)

To run the service in a container, you can use the following commands:


For CPU:

```bash
bentoml build -f bentofile.yaml
```

```bash
bentoml containerize foodgenius-service:latest
```

```bash
docker run -p 3000:3000 foodgenius-service:$(bentoml get foodgenius-service:latest | yq -r ".version")
```

For GPU:

```bash
bentoml build -f bentofile.gpu.yaml
```

```bash
bentoml containerize foodgenius-service-gpu:latest 
```

```bash
docker run --gpus all -p 3000:3000 foodgenius-service-gpu:$(bentoml get foodgenius-service-gpu:latest | yq -r ".version")
```

> Note that to run with GPU you will need to have [nvidia-container-runtime](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) setup.

### Python API

You can also use the service as a Python API:

````bash
bentoml build -f bentofile.yaml
````

then start the service:
```python
import bentoml

bento = bentoml.get('foodgenius-service:latest')

server = bentoml.HTTPServer(bento, port=3000)
server.start(blocking=True)
```

## 🌐 Using the Service 🌐
You can use the BentoML service with HTTP requests. Here are some examples:

### cURL
The following example shows how to send a request to the service to classify an image via cURL:

```bash
curl -X POST \ 
  'http://0.0.0.0:3000/classify' \   
  -H "Content-Type: multipart/form-data" \  
  -F "img=@examples/images/pizza.jpg"
```

### BentoML Client

To send requests via client using python library:

```python
IMG_PATH = "examples/images/pizza.jpg"

if __name__ == "__main__":
    import bentoml

    client = bentoml.SyncHTTPClient("http://localhost:3000")

    print("Predictions for image {}".format(IMG_PATH))
    print(client.classify(img=IMG_PATH))

    client.close()
```

## 🏋️‍♂️ Training and Prediction 🏋️‍♂️

Before running the scripts/notebooks, it's recommended to create a new environment:

```bash
conda env create -f environment.yml
conda activate foodgenius
```

### Training

You can train the models using the `train.py` script. Here are the steps:

1. Train the `food_or_nonfood` model:
    ```bash
    python train.py \ 
    --model food_or_nonfood \
    --epochs 5 \
    --model_name pretrained_effnetb2_food_or_nonfood.pth \ 
    --split_size 1 \
    --batch_size 32 \ 
    --learning_rate 0.001 \
    --device cuda # or cpu
    ```

2. Train the `food101` model:
    ```bash
    python train.py \ 
    --model food101 \ 
    --epochs 10 \ 
    --model_name pretrained_effnetb2_food101.pth \ 
    --split_size 0.2 \ 
    --batch_size 32 \ 
    --learning_rate 0.001 \
    --device cuda # or cpu
    ```

> Use device `cuda` if you have a GPU compatible available.

Results for the training process including accuracy, loss will be saved in the `results` directory.

#### Training Hyperparameters

| Parameter     | Default                                      | Description       |
|---------------|--------------------------------------------------|---------------------|
| `epochs`    | `5`                                       | Number of epochs for training       |
| `batch_size` | `32`                                      | Batch size for training             |
| `split_size` | `0.2`                                     | Train-test split size |
| `device`     | `cuda`                                    | Device for training (`cuda` or `cpu`) |
| `learning_rate`         | `0.001`                                   | Learning rate for training          |
| `model_name` | `model.pth` | Name of the trained model file      |	

#### Model Output Directory Structure

```
results/
│
└── food101/
|   └── model_name
|       ├── model.pth
│       ├── model_results.csv
│       └── model_results.png
└── food_or_nonfood/
|   └── model_name
|       ├── model.pth
│       ├── model_results.csv
│       └── model_results.png
```

### Prediction

You can make predictions using the `predict.py` script. Here are the steps:

1. Predict using the `food_or_nonfood` model:
    ```bash
    python predict.py \ 
    --model food_or_nonfood \ 
    --image path/to/image.jpg \ 
    --model_path models/pretrained_effnetb2_food_or_nonfood.pth \ 
    --device cpu
    ```

2. Predict using the `food101` model:
    ```bash
    python predict.py \ 
    --model food101 \ 
    --image path/to/image.jpg \ 
    --model_path models/pretrained_effnetb2_food101.pth \
    --device cpu
    ```

## 📓 Jupyter Notebooks 📓

This repository includes several Jupyter Notebooks that demonstrate the training and prediction processes using EfficientNetB2.

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

To deploy the service to k8s, you can use the following commands:

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

## 📊 Observability 📊

BentoML provides built-in observability features, including Prometheus metrics. You can access these metrics at the `/metrics` endpoint.

To install monitoring stack on kubernetes, you can do the following steps:

### Quick setup


```bash
chmod +x scripts/setup_monitoring.sh; ./scripts/setup_monitoring.sh
```

This script will install prometheus + grafana stack on namespace monitoring.


Access grafana dashboard (default username/password is `admin`):

```bash
kubectl port-forward svc/grafana -n monitoring 3000:3000
```

![](assets/images/grafana.jpg)


## 📝 Author
**Davi Araujo (@daviaraujocc)**

## TODOS

- [ ] Automate training/deploy via ArgoCD Workflows + GitOps
