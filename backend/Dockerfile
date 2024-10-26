# Use the official FastAPI image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy project
COPY . /app
