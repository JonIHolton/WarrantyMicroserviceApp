import pika
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define SMTP email server details
smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_username = 'your_username'
smtp_password = 'your_password'

# Define the connection parameters to the RabbitMQ server
amqp_url = 'your_amqp_broker_url'
params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declare the queue in case it doesn't exist
channel.queue_declare(queue='email_notifications')

def send_email(recipient, subject, message):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server and send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection
    server.login(smtp_username, smtp_password)
    server.send_message(msg)
    server.quit()

def callback(ch, method, properties, body):
    email_data = json.loads(body)
    send_email(email_data['email'], email_data['subject'], email_data['message'])

# Set up consumption of messages from the 'email_notifications' queue
channel.basic_consume(queue='email_notifications', on_message_callback=callback, auto_ack=True)

print('Email Service is running. To exit press CTRL+C')
try:
    # Start consuming messages
    channel.start_consuming()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    print('Email Service has stopped')
