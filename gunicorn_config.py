import os

# The port to bind Gunicorn to, typically set via environment variable or default to 80
port = os.getenv("PORT", "80")

# Maximum number of requests a worker can handle before being restarted
max_requests = 0  # Set to 0 for no limit, or specify a number for controlled restarts
max_requests_jitter = 10  # Random jitter to prevent all workers from restarting at once

# Bind to all available network interfaces (0.0.0.0) and the specified port
bind = f"0.0.0.0:{port}"

# Number of worker processes to handle requests. The number of workers is typically set to the number of CPU cores.
workers = os.getenv("GUNICORN_WORKERS", 1)  # Default to 1 worker unless specified in env var

# Timeout for worker connections (in seconds)
timeout = 180  # Adjust based on your app's response time needs (default is 30 seconds)

# Change the working directory to the 'app' folder.
# This is important if your FastAPI app resides in a subdirectory.
chdir = "./app"  # Adjust this path based on your project structure

# Logging settings (optional but recommended for debugging and production monitoring)
accesslog = "-"  # Logs HTTP access to stdout
errorlog = "-"  # Logs errors to stdout
loglevel = "info"  # Adjust the log level (debug, info, warning, error, critical)
