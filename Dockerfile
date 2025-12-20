# Update 1: Use a newer Python version (faster, more secure)
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (GCC is needed for some python libraries)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Update 2: Copy everything at once. 
# This is safer than copying folders individually because it preserves 
# your exact folder structure (e.g. if static is inside src or outside).
COPY . .

# Create data directory explicitly to avoid permission errors
RUN mkdir -p /app/src/data

# Environment variables
ENV FLASK_APP=src/app.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Update 3: Run the file directly
# This ensures it uses the host='0.0.0.0' settings you wrote in your python code
CMD ["python", "src/app.py"]