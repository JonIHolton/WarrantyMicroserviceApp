import amqp_connection
import json
import pika
import os
from postmarker.core import PostmarkClient
#from os import environ

e_queue_name = 'Email'        # queue to be subscribed by Error microservice
client = PostmarkClient(server_token='5200ad5e-6357-4739-9c62-36bf526301fc')

from_email = 'darrell.tan.2022@scis.smu.edu.sg'
to_email = 'darrell.tan.2022@scis.smu.edu.sg'
subject = 'ESD Rabak'
body = 'This is a test email sent using Postmark.'

def receiveError(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=e_queue_name, on_message_callback=callback, auto_ack=True)
        print('error microservice: Consuming from queue:', e_queue_name)
        channel.start_consuming() # an implicit loop waiting to receive messages; 
        #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

    except pika.exceptions.AMQPError as e:
        print(f"error microservice: Failed to connect: {e}") 

    except KeyboardInterrupt:
        print("error microservice: Program interrupted by user.")

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nerror microservice: Received an error by " + __file__)
    processError(body)
    print()

def processError(errorMsg):
    print("error microservice: Printing the error message:")
    try:
        error = json.loads(errorMsg)
        print("--JSON:", error)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", errorMsg)
    print()

def sendEmail():
    response = client.emails.send(
    From=from_email,
    To=to_email,
    Subject=subject,
    HtmlBody=body
)
    # Check if the email was sent successfully
    if response["ErrorCode"] == 0:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email. Error: {response.Message}")  

if __name__ == "__main__": # execute this program only if it is run as a script (not by 'import')    
    print("email microservice: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("error microservice: Connection established successfully")
    channel = connection.channel()
    receiveError(channel)
