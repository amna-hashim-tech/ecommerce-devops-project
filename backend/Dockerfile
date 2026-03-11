# Start with Python 3.10 base image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (Docker caching optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port 5000
EXPOSE 5000

# Run the app with gunicorn (production server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]