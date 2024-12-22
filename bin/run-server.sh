#!/bin/bash
set -e

cd $APP_HOME

gunicorn server:server -k uvicorn_workers.AsyncioUvicornWorker --config ./gunicorn_config.py
