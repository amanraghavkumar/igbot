FROM python:3.12-slim

# Install system dependencies needed by moviepy
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Debug check for moviepy installation
RUN python -c "import moviepy.editor; print('✅ moviepy installed')"

# Copy project files
COPY . .

# Run your bot
CMD ["python", "bot.py"]
