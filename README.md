pip install -r requirements/cpu-requirements.txt

bentoml serve service:FoodGenius

curl -X POST "http://127.0.0.1:3000/classify"   -H "Content-Type: multipart/form-data"   -F "i
mg=@examples/images/pizza.jpg" |  jq -r '.predictions | to_entries | max_by(.value) | .key'


