# fastapi_auth_service/Dockerfile

# 1️⃣ Base Image
FROM python:3.10-slim
# We use a slim Python image to reduce image size but still have all core Python features.

# 2️⃣ Set working directory in the container
WORKDIR /app
# This is where all commands will be run inside the container (like cd /app).

# 3️⃣ Copy requirements.txt into container
COPY requirements.txt ./
# We first copy only the requirements to take advantage of Docker layer caching.

# Install dependencies
RUN apt-get update && apt-get install -y netcat-openbsd

# 4️⃣ Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Installs dependencies defined in requirements.txt. "--no-cache-dir" avoids keeping pip cache in the image.

# 5️⃣ Copy the rest of the FastAPI code into container
COPY . .
# This will copy everything else from your fastapi_auth_service directory into the container.

# 6️⃣ Expose the port FastAPI runs on
EXPOSE 8000
# Tells Docker that this container will listen on port 8000 (used in docker-compose).

# 7️⃣ Run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# This is the default command to run the FastAPI app inside the container.
