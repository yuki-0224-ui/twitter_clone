FROM python:3.12

RUN apt-get update && apt-get install -y \
        chromium \
        chromium-driver

ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
