# Use the official Python image
FROM python:3.10.8

# Set an environment variable to prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any required packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5002 to the host machine
EXPOSE 5002

# Start the application
CMD ["python", "server.py"]
