# Use slim Python image
FROM python:3.12-slim

# Install system dependencies (ffmpeg is critical for moviepy)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Expose port (optional, in case you run a webserver later)
EXPOSE 8000

# Start the bot
CMD ["python", "bot.py"]
