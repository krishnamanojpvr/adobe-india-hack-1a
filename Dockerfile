
FROM python:3.10-alpine AS base

# Install required system libraries
RUN apk add --no-cache libstdc++

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY . /app

# Default command
CMD ["python", "process_pdfs.py"]
