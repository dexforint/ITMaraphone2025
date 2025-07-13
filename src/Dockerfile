# ---- build stage -------------------------------------------------
FROM python:3.11-slim

# 1. Обновляем pip
RUN pip install --no-cache-dir --upgrade pip

# 2. Копируем исходники и зависимости
WORKDIR /app
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src /app

# 3. Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    GIGACHAT_API_KEY="<<PUT_YOUR_KEY_AT_RUNTIME>>" \
    PORT=8080

EXPOSE 8080

# 4. Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]