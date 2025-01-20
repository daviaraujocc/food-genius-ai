<div align="center">
    <h1 align="center">Food Genius AI</h1>
    <br>
    <strong>Uma aplicação poderosa de IA construída usando EfficientNetB2 que pode detectar o tipo de alimento em uma imagem e determinar se a imagem contém alimento ou não.<br></strong>
    <i>Desenvolvido por BentoML 🍱</i>
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

## 🏃‍♂️ Executando o Serviço 🏃‍♂️
Para aproveitar ao máximo este repositório, recomendamos que você o clone e experimente o serviço localmente.

Isso requer Python 3.11+ e `pip` instalado.

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

### Containers

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

> Para uso de GPU, utilize `bentofile.gpu.yaml` e `requirements/gpu-requirements.txt`.

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

## 🚀 Deploy para o kubernetes 🚀

Para o deploy do serviço em produção, você pode usar os seguintes comandos:

```bash
bentoml build -f bentofile.yaml
```

```bash
bentoml containerize foodgenius-service:latest --image-tag {seu-usuario-repo}/foodgenius-service:latest
```

```bash
docker push {your-username-repo}/foodgenius-service:latest
```

Edite o arquivo `manifests/deployment.yaml` para incluir sua imagem, depois aplique-o ao seu cluster Kubernetes:
```bash
kubectl apply -f manifests/deployment.yaml
```


## 📓 Jupyter Notebooks 📓

Este repositório inclui vários Jupyter Notebooks que demonstram os processos de treinamento e predição usando EfficientNetB2.

### Notebooks de Treinamento

1. **Treinamento EfficientNetB2 para Classificação de Alimentos ou Não-Alimentos**
    - Arquivo: [effnetb2_training_food_or_nonfood.ipynb](effnetb2_training_food_or_nonfood.ipynb)
    - Descrição: Este notebook treina um modelo no Dataset Food5K para classificar imagens como alimentos ou não-alimentos usando a arquitetura EfficientNetB2.

2. **Treinamento EfficientNetB2 para o Dataset Food101**
    - Arquivo: [effnetb2_training_food101.ipynb](effnetb2_training_food101.ipynb)
    - Descrição: Este notebook treina um modelo no dataset Food101 para classificar diferentes tipos de alimentos usando a arquitetura EfficientNetB2.

### Notebook de Predição

1. **EfficientNetB2 Predição**
    - Arquivo: [effnetb2_predict.ipynb](effnetb2_predict.ipynb)
    - Descrição: Este notebook demonstra como usar o modelo EfficientNetB2 treinado para fazer predições em novas imagens.

Sinta-se à vontade para explorar esses notebooks para entender os fluxos de trabalho de treinamento e predição em detalhes.

## 📝 Autor
**Davi Araujo (@daviaraujocc)**
