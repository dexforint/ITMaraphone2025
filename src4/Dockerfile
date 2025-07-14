FROM python:3.11-slim AS base

# сочтимся с pdf, т.к. нужен build-essential для некоторых колёс
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ------------------ stage 2: copy src -----------------
COPY . /app

# чтобы print'ы сразу шли в лог
ENV PYTHONUNBUFFERED=1 \
    GIGA_URL="https://gigachat.devices.sberbank.ru/api/v1"

EXPOSE 8080

# ------------------ entrypoint ------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]