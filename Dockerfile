# Use an official Python runtime as a parent image
FROM python:latest

# Set environment variables to prevent Python from writing pyc files to disc and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /tor-python-crawler

# Install Tor
RUN apt-get update && apt-get install -y tor torsocks \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container at /tor-python-crawler
COPY app/requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local app directory to the container
COPY app .

# Expose port for debugging purposes
EXPOSE 5678

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Give execution rights on the entrypoint script
RUN chmod +x /entrypoint.sh

# Set the entrypoint script to be executed
ENTRYPOINT ["/entrypoint.sh"]

# Default command to run when starting the container
CMD ["python", "./script.py"]