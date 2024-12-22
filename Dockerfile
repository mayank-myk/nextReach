FROM --platform=linux/amd64 python:3.9-slim
ENV DEBIAN_FRONTEND noninteractive
ENV APP_HOME /app
RUN apt-get update && apt-get install gcc -y && apt-get clean
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
COPY poetry.lock pyproject.toml ./
RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi
ENV PYTHONPATH $APP_HOME
ADD referral-recommendation-master $APP_HOME
CMD ["./bin/run-server.sh"]
