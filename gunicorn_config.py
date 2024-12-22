import os

port = os.getenv("PORT", "80")
max_requests = 0
max_requests_jitter = 10
bind = "0.0.0.0:%s" % port
workers = 1  # Increase the workers once we have a reliable way to forward health checks to all the workers.
timeout = 180
chdir = "./app"
