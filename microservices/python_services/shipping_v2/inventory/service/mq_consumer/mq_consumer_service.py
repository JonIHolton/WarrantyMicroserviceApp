import pika
import json

class MQConsumerService:
    def __init__(self, host, queue_name):
        self.host = host
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name,durable=True)

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=self.message_callback,
                                   auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def message_callback(self, ch, method, properties, body):
        print(f" [x] Received {body}")
        try:
            message = json.loads(body)
            print(f"Processed message: {message}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def close_connection(self):
        self.connection.close()