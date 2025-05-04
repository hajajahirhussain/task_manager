# Dockerfile for Django app (taskmanager)

# 1. Use official Python slim image
FROM python:3.10-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd

# 4. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Django project files to the container
COPY . .

# 6. Collect static files (prepare for future static use with whitenoise)
# RUN python manage.py collectstatic --noinput
COPY wait-for-it.sh entrypoint.sh ./
RUN chmod +x wait-for-it.sh entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]


# 7. Set Django & Python runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 8. Expose port
EXPOSE 8000

# 9. Start Django with Gunicorn (handled in entrypoint.sh)
# CMD ["gunicorn", "taskmanager.wsgi:application", "--bind", "0.0.0.0:8000"]
