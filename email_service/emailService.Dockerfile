# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app 

# Copy the current directory contents into the container at /app
COPY ./requirements.txt ./ 

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./emailService.py  ./amqp_connection.py ./amqp_setup.py ./


# Run the Python script when the container launches
CMD ["python", "emailService.py"]
