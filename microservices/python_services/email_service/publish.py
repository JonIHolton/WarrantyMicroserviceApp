import pika
import json
import amqp_connection

import os, sys
from os import environ

exchangename = "warranty_service" # exchange name
exchangetype="topic" # use a 'topic' exchange to enable interaction

# Instead of hardcoding the values, we can also get them from the environ as shown below
# exchangename = environ.get('exchangename') #order_topic
# exchangetype = environ.get('exchangetype') #topic 

#create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection() 
channel = connection.channel()

if not amqp_connection.check_exchange(channel, exchangename, exchangetype):
    print("\nCreate the 'Exchange' before running this microservice. \nExiting the program.")
    sys.exit(0)  # Exit with a success status

sample_data={
    "request_Id": "0002",
    "status": "valid",
    "claimee": "Darrell",
    "email":"jholton.2022@scis.smu.edu.sg"
}
message=json.dumps(sample_data)

channel.basic_publish(exchange=exchangename, routing_key="warranty.update", 
    body=message, properties=pika.BasicProperties(delivery_mode = 2))