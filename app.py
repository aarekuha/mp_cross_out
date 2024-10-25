import sys
import json
import logging
import logging.handlers
import queue
import random
import string
import threading
from contextlib import suppress

from fastapi import FastAPI

app = FastAPI()

# # Configure logging to output to stderr
logger = logging.getLogger("json_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
formatter = logging.Formatter('%(message)s')  # Output only the message
handler.setFormatter(formatter)
logger.addHandler(handler)


class CustomQueueHandler(logging.handlers.QueueHandler):
    def enqueue(self, record):
        with suppress(queue.Full):
            return super().enqueue(record)


def setup_queue_logging(log_queue):
    """
    Глобальная настройка логирования с использованием QueueHandler.
    Все сообщения логов будут отправляться в очередь.
    """
    # Создаем QueueHandler и добавляем его к корневому логгеру
    queue_handler = CustomQueueHandler(log_queue)
    root_logger = logging.getLogger()

    # Удаляем все другие обработчики у корневого логгера
    # Это необходимо, чтобы избежать дублирования сообщений
    global logger
    for handler in logger.handlers:
        logger.removeHandler(handler)

    root_logger.setLevel(logging.DEBUG)  # Установите желаемый уровень логирования
    root_logger.addHandler(queue_handler)
    root_logger.propagate = True

    logger = root_logger


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
    if getattr(app, "logger_queue", None):
        setup_queue_logging(app.logger_queue)
    thread = threading.Thread(target=generate_large_json, daemon=True)
    thread.start()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
