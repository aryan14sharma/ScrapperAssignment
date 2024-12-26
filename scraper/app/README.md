To install dependencies run command -
 pip install -r requirements.txt 

Run redis image on docker using command -
    docker run --name redis -p 6379:6379 -d redis

To run service use command -
    python main.py

Sample Curl -
    curl --location 'http://localhost:8000/scrape' \
    --header 'Authorization: Bearer iambatman' \
    --header 'Content-Type: application/json' \
    --data '{"pages": 1, "proxy": null}'
