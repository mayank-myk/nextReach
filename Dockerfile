FROM --platform=linux/amd64 python:3.11-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV APP_HOME=/app
ENV PYTHONPATH=$APP_HOME

# Update the package list and install gcc for compiling dependencies (if needed)
RUN apt-get update && apt-get install -y gcc && apt-get clean

# Create and set the working directory
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Copy poetry files to install dependencies
COPY poetry.lock pyproject.toml ./

# Upgrade pip, install poetry, configure poetry to avoid creating a virtual environment, and install dependencies
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the application code (change this path as needed based on your repo structure)
COPY . .

# Ensure the correct permissions for your startup script
RUN chmod +x ./bin/run-server.sh

# Default command to run the application
CMD ["./bin/run-server.sh"]
