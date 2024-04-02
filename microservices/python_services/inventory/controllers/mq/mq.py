# app.py or wherever your Flask app is initialized
from flask import Flask, request, jsonify, current_app

from service.mq_product.mq_producer_service import MQProducerService


from . import api_mq

@api_mq.route('/send_message', methods=['POST'])
def send_message():
    message_content = request.json.get('message')
    if not message_content:
        return jsonify({'error': 'No message provided'}), 400

    host = current_app.config['RABBITMQ_HOST']
    queue_name = current_app.config['RABBITMQ_QUEUE']

    producer = MQProducerService(host, queue_name)
    try:
        producer.send_message(message_content)
        return jsonify({'status': 'success', 'message': 'Message sent successfully'}), 200
    finally:
        producer.close_connection()


