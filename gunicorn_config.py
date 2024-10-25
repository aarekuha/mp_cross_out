import logging
from logging.handlers import QueueListener
from multiprocessing import Queue


log_queue = Queue(maxsize=10_000)

# gunicorn.conf.py
def post_fork(server, worker):
    worker.app.wsgi().logger_queue = log_queue


stream_handler = logging.StreamHandler()
queue_listener = QueueListener(log_queue, stream_handler)
queue_listener.start()


# Set the log level to critical to minimize output
loglevel = 'critical'
# Disable access log
accesslog = None
# Disable error log
errorlog = None
# Do not capture output
capture_output = False
# Number of worker processes
workers = 4
# Worker class
worker_class = 'uvicorn.workers.UvicornWorker'

# Write PID to a file for process management
pidfile = 'gunicorn.pid'

