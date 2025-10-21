FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости ОДИН РАЗ при сборке
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Точка входа — будет запускать скрипт из volume
CMD ["python", "netflix.py"]