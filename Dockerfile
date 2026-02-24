FROM python:3.10

WORKDIR /app

RUN apt-get update -o Acquire::Retries=3 && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
                --timeout 300 \
                --retries 25 \
                -r requirements.txt

COPY . .