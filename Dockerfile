FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --progress-bar off --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]