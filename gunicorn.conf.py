import os

# Render dynamically injects PORT (defaults to 5000 for local runs)
port = os.environ.get("PORT", "5000")
bind = f"0.0.0.0:{port}"

# Concurrency & worker configuration
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
threads = int(os.environ.get("GUNICORN_THREADS", "2"))
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "120"))
keepalive = 5
preload_app = True

# Logging to standard output/error for Render log console
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info")
