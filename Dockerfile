FROM python:3.10-bullseye

WORKDIR /app

COPY . .

RUN pip install --progress-bar off --no-cache-dir -r requirements.txt



