#!/bin/bash
set -e

# Ensure we're in the correct directory
cd $APP_HOME

# Run Gunicorn using the custom worker from server.py
exec gunicorn server:server \
  -k uvicorn.workers.UvicornWorker \
  --config ./gunicorn_config.py \
  "$@"
