# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api.py promotion_model.pkl ./

# Expose port (Cloud Run will set PORT environment variable)
ENV PORT=8080

# Run the application
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port $PORT"]