# app.py or wherever your Flask app is initialized
import json
from flask import request, jsonify, current_app
import pika

from service.mq_product.mq_producer_service import MQProducerService


from . import api_mq


@api_mq.route('/send_message', methods=['POST'])
def send_email():
    try:
        email_data = request.json
        message = email_data.get('message')

        if not message:
            return jsonify({'error': 'Message is required'}), 400

        # RabbitMQ connection
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=current_app.config['RABBITMQ_HOST']))
        channel = connection.channel()

        # Make sure the queue exists
        channel.queue_declare(queue=current_app.config['RABBITMQ_QUEUE'], durable=True)


        body = json.dumps(message)
        # Send message to queue
        channel.basic_publish(
            exchange='',
            routing_key='Email',
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2, 
            ))
        
        
        connection.close()

        return jsonify({'status': 'success', 'message': 'Email sent successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


