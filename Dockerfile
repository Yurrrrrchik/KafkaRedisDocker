FROM python:3.10-bullseye

WORKDIR /app

COPY processes_classes processes_classes

COPY main.py .

COPY requirements.txt .

RUN pip install --progress-bar off --no-cache-dir -r requirements.txt



