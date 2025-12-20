FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY static/ ./static/
COPY templates/ ./templates/  

RUN mkdir -p /app/src/data

ENV FLASK_APP=src/app.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]