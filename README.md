<div align="center">
    <h1 align="center">Food Genius AI</h1>
    <br>
    <strong>A powerful AI application built using EfficientNetB2 that can detect the type of food in an image and determine whether the image contains food or not.<br></strong>
    <i>Powered by BentoML 🍱</i>
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

## 🏃‍♂️ Running the Service 🏃‍♂️
To fully take advantage of this repo, we recommend you to clone it and try out the service locally. 

This requires Python3.11+ and `pip` installed.

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

### Containers

To run the service in a container, you can use the following commands:

```bash
bentoml build -f bentofile.yaml
```

```bash
bentoml containerize foodgenius-service
```

```bash
docker run -p 3000:3000 foodgenius-service:$(bentoml get foodgenius-service:latest | yq -r ".version")
```

> For GPU use bentofile.gpu.yaml and requirements/gpu-requirements.txt.

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

## 🚀 Deploying to Production 🚀




```bash
bentoml build
```



```bash
bentoml push <name:version>
```

## 📝 Author
**Davi Araujo (@daviaraujocc)**