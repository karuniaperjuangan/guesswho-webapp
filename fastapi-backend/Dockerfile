# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    telnet \ 
    wkhtmltopdf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# Copy the current directory contents into the container at /app
COPY ./fastapi-backend/requirements.txt .

RUN ls

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install onnxruntime

COPY ./vector-database /vectordb
COPY ./fastapi-backend/ .
# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME=FastAPI

# Run app.py when the container launches
CMD ["fastapi", "run", "main.py", "--port", "8000"]