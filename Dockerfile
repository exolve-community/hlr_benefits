# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы приложения
COPY . .

# Открываем порт для Flask
EXPOSE 7002

# Команда запуска приложения
CMD ["python", "app.py"]
