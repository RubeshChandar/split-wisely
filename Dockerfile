FROM python:3.11

# This line prevents django by writing the pyc files inside container which aren't necessary
ENV PYTHONDONTWRITEBYTECODE = 1 
# Sends logs to container without buffering (Kind of convention to add in every python image)
ENV PYTHONUNBUFFERED = 1

WORKDIR /app 

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000