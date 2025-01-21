import bentoml

IMG_PATH = "examples/images/pizza.jpg"

if __name__ == "__main__":
    

    client = bentoml.SyncHTTPClient("http://localhost:3000")

    print("Predictions for image {}".format(IMG_PATH))
    print(client.classify(img=IMG_PATH))

    client.close()