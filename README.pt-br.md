<div align="center">
    <h1 align="center">Food Genius AI</h1>
    <br>
    <strong>Uma aplicação poderosa de IA construída usando EfficientNetB2 que pode detectar o tipo de alimento em uma imagem e determinar se a imagem contém alimento ou não.<br></strong>
    <i>Desenvolvido com BentoML 🍱 e PyTorch 🔥</i>
    <br>
</div>
<br>

<div align="center">
    <a href="README.md">🇺🇸 English</a> | <a href="README.pt-br.md">🇧🇷 Português (Brasil)</a>
</div>
<br>

## 📖 Introdução 📖
FoodGeniusAI é uma aplicação alimentada por IA que usa EfficientNetB2 para classificar imagens de alimentos. Ela pode identificar o tipo de alimento e determinar se a imagem contém alimento.

<div align="center">
    <img src="https://github.com/daviaraujocc/food-genius-ai/blob/main/assets/images/demo.gif" alt="demo" >   
</div>

### 📊 Modelos 📊
FoodGeniusAI usa dois modelos principais para classificação:

1. **Modelo Alimento ou Não-Alimento (Food5K)**
    - Este modelo classifica imagens como alimento ou não-alimento usando o dataset Food5K.

2. **Modelo Food101**
    - Este modelo classifica imagens em 101 diferentes tipos de alimentos usando o dataset Food101.

Ambos os modelos são baseados na arquitetura EfficientNetB2 e foram treinados usando PyTorch. Modelos pré-treinados estão localizados no diretório `models`.

## Glossário
- [Requisitos](#-requisitos-)
- [Executando o Serviço](#-executando-o-serviço-)
- [Usando o Serviço](#-usando-o-serviço-)
- [Aplicativo no Hugging Face](#-aplicativo-no-hugging-face-)
- [Treinamento e Predição](#-treinamento-e-predição-)
- [Jupyter Notebooks](#-jupyter-notebooks-)
- [Deploy para Kubernetes](#-deploy-para-kubernetes-)

## 📋 Requisitos 📋

- Python 3.11+
- BentoML
- Pip

## 🏃‍♂️ Executando o Serviço 🏃‍♂️
> Para uso de GPU, utilize `bentofile.gpu.yaml` e `requirements/gpu-requirements.txt`.

1. Clone o repositório:
    ```bash
    git clone https://github.com/daviaraujocc/FoodGeniusAI.git
    cd FoodGeniusAI
    ```

2. Instale as dependências:
    ```bash
    pip install -r requirements/cpu-requirements.txt
    ```

3. Sirva o serviço BentoML:
    ```bash
    bentoml serve 
    ```

Você pode então abrir seu navegador em http://127.0.0.1:3000 e interagir com o serviço através do Swagger UI.


### 🐳 Containers 🐳

Para executar o serviço em um container, você pode usar os seguintes comandos:

```bash
bentoml build -f bentofile.yaml
```

> Executar este comando criará no home do usuário, o diretório `bentoml` com os arquivos do serviço.

```bash
bentoml containerize foodgenius-service
```

```bash
docker run -p 3000:3000 foodgenius-service:$(bentoml get foodgenius-service:latest | yq -r ".version")
```



## 🌐 Usando o Serviço 🌐
Você pode usar o serviço BentoML com requisições HTTP. Aqui estão alguns exemplos:

### cURL
O exemplo a seguir mostra como enviar uma requisição para o serviço para classificar uma imagem via cURL:

```bash
curl -X POST \ 
  'http://127.0.0.1:3000/classify' \   
  -H "Content-Type: multipart/form-data" \  
  -F "img=@examples/images/pizza.jpg"
```

## 🤗 Aplicativo no Hugging Face 🤗

Você também pode experimentar a aplicação FoodGeniusAI no Hugging Face Spaces:

[FoodGeniusAI no Hugging Face](https://huggingface.co/spaces/daviaraujocc/foodgeniusai)



## 🏋️‍♂️ Treinamento e Predição 🏋️‍♂️

### Treinamento

Você pode treinar os modelos usando o script `train.py`. Aqui estão os passos:

1. Treine o modelo `food_or_nonfood`:
    ```bash
    python train.py --model food_or_nonfood --epochs 10 --model_name pretrained_effnetb2_food_or_nonfood.pth --batch_size 32 --device cpu
    ```

2. Treine o modelo `food101`:
    ```bash
    python train.py --model food101 --epochs 5 --model_name pretrained_effnetb2_food101.pth --split_size 0.2 --batch_size 32 --device cpu
    ```

### Predição

Você pode fazer predições usando o script `predict.py`. Aqui estão os passos:

1. Predição usando o modelo `food_or_nonfood`:
    ```bash
    python predict.py --model food_or_nonfood --image path/to/image.jpg --model_path models/pretrained_effnetb2_food_or_nonfood.pth --class_names_path class_names.txt --device cuda
    ```

2. Predição usando o modelo `food101`:
    ```bash
    python predict.py --model food101 --image path/to/image.jpg --model_path models/pretrained_effnetb2_food101.pth --class_names_path class_names.txt --device cuda
    ```

## 📓 Jupyter Notebooks 📓

Este repositório inclui vários Jupyter Notebooks que demonstram os processos de treinamento e predição usando EfficientNetB2.

Antes de rodar os notebooks, instale as dependências usando conda ou venv:

```bash
conda env create -f environment.yml
conda activate foodgenius
```

### Notebooks de Treinamento

1. **Classificação de Alimentos ou Não-Alimentos**
    - [effnetb2_training_food_or_nonfood.ipynb](effnetb2_training_food_or_nonfood.ipynb)
    - Treina um modelo no dataset Food5K para classificar imagens como alimentos ou não-alimentos.

2. **Classificação Food101**
    - [effnetb2_training_food101.ipynb](effnetb2_training_food101.ipynb)
    - Treina um modelo no dataset Food101 para classificar imagens em 101 tipos de alimentos.

### Notebook de Predição

1. **EfficientNetB2 Predição**
    - [effnetb2_predict.ipynb](effnetb2_predict.ipynb)
    - Demonstra como usar o modelo EfficientNetB2 treinado para fazer predições em novas imagens.

## 🚀 Deploy para Kubernetes 🚀

Para o deploy do serviço em produção, você pode usar os seguintes comandos:

```bash
bentoml build -f bentofile.yaml
```

```bash
bentoml containerize foodgenius-service:latest --image-tag {seu-usuario-repo}/foodgenius-service:latest
```

```bash
docker push {seu-usuario-repo}/foodgenius-service:latest
```

Edite o arquivo `manifests/deployment.yaml` para incluir sua imagem, depois aplique-o ao seu cluster Kubernetes:
```bash
kubectl apply -f manifests/deployment.yaml
```

## 📝 Autor
**Davi Araujo (@daviaraujocc)**
