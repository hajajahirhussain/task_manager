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

# 6. Handle environment variables (from GitHub Secrets via build args)
ARG SECRET_KEY
ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG FASTAPI_AUTH_URL

ENV SECRET_KEY=$SECRET_KEY \
    DB_NAME=$DB_NAME \
    DB_USER=$DB_USER \
    DB_PASSWORD=$DB_PASSWORD \
    DB_HOST=$DB_HOST \
    DB_PORT=$DB_PORT \
    FASTAPI_AUTH_URL=$FASTAPI_AUTH_URL

# 7. Collect static files (prepare for future static use with whitenoise)
RUN python manage.py collectstatic --noinput

# 8. Set Django & Python runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 9. Expose port
EXPOSE 8000

# 10. Start Django with Gunicorn
CMD ["gunicorn", "taskmanager.wsgi:application", "--bind", "0.0.0.0:8000"]
