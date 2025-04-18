FROM python:3.11-slim

# This line prevents django by writing the pyc files inside container which aren't necessary
ENV PYTHONDONTWRITEBYTECODE=1 
# Sends logs to container without buffering (Kind of convention to add in every python image)
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app 

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000