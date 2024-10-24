from fastapi import FastAPI
import threading
import logging
import json
import sys
import random
import string

app = FastAPI()

# Configure logging to output to stderr
logger = logging.getLogger("json_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(message)s')  # Output only the message
handler.setFormatter(formatter)
logger.addHandler(handler)

# Функция генерации большого JSON
def _generate_large_json(num_fields=1000, field_length=20):
    return {
        f'field_{i}': ''.join(random.choices(string.ascii_letters + string.digits, k=field_length))
        for i in range(num_fields)
    }


data = _generate_large_json()
with open("example.out", "wb") as f:
    f.write(str(data).encode())


def generate_large_json():
    while True:
        # Generate a large JSON message
        json_str = json.dumps(data)
        logger.info(json_str)

# Start the background thread when the app starts
@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=generate_large_json, daemon=True)
    thread.start()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
