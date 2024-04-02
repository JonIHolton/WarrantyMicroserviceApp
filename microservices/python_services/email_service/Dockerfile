# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app 

# Copy the current directory contents into the container at /app
COPY ./requirements.txt ./ 

# Install any needed dependencies specified in requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY ./amqp_setup.py ./amqp_setup.py
COPY ./email_service.py ./amqp_connection.py ./


# Run the Python script when the container launches
CMD ["python", "./email_service.py"]
