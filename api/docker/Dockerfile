FROM python:3.11-slim-buster
RUN adduser --system --no-create-home app \
    && apt-get update \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /usr/src/app
COPY ./dataset ./ds
ENV PYTHONPATH "${PYTHONPATH}:/usr/src"
COPY requirements.txt .
RUN ["pip", "install", "-r", "requirements.txt", "--upgrade"]
COPY ./app .
USER app
CMD ["python", "main.py"]
