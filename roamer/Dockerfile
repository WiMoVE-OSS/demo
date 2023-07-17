FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
RUN apt update && apt install wpasupplicant -y
COPY ./app /app
