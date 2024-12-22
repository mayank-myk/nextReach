#!/bin/bash
set -e

# Ensure we're in the correct directory
cd $APP_HOME

# Run Gunicorn using the custom worker from server.py
exec gunicorn server:app \
  -k server.AsyncioUvicornWorker \
  --config ./gunicorn_config.py \
  "$@"

