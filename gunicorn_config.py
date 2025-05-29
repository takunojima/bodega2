import os

# Worker Processes
workers = int(os.environ.get('GUNICORN_WORKERS', 4))
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5

# Server Mechanics
preload_app = True

# Server Socket
bind = "0.0.0.0:" + os.environ.get("PORT", "10000")

# Logging
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
loglevel = 'info'

# Server Hooks
def on_starting(server):
    server.log.info("Starting Gunicorn Server") 