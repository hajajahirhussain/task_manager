# Dockerfile for Django app (taskmanager)

# 1. Use official Python slim image
FROM python:3.10-slim

# 2. Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y netcat-openbsd

# 3. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy Django project files to the container
COPY . .

# 5. Collect static files (prepare for future static use with whitenoise)
RUN python manage.py collectstatic --noinput

# 6. Environment variables (optional optimizations)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 7. Expose port 8000 for the app
EXPOSE 8000

# 8. Command to run Django via Gunicorn
CMD ["gunicorn", "taskmanager.wsgi:application", "--bind", "0.0.0.0:8000"]
