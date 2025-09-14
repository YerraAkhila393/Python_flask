# Base image
FROM python:3.12-slim


# Set working directory
WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Environment variables
ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1

# Expose Flask port
EXPOSE 5001

# Run with Gunicorn (production-ready WSGI server)
# Run Flask app
CMD ["python","-m", "app"]