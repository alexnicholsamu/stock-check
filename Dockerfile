# Use the official Python 3.9 image based on Alpine
FROM python:3.9-alpine

# Set the working directory
WORKDIR /stock-check-app

# Copy application files into the container
COPY . /stock-check-app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Set the entry point or command to run when the container starts
CMD ["python", "wsgi.py"]
