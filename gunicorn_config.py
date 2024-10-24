# gunicorn.conf.py

# Set the log level to critical to minimize output
loglevel = 'critical'
# Disable access log
accesslog = None
# Disable error log
errorlog = None
# Do not capture output
capture_output = False
# Number of worker processes
workers = 2
# Worker class
worker_class = 'uvicorn.workers.UvicornWorker'

# Write PID to a file for process management
pidfile = 'gunicorn.pid'

