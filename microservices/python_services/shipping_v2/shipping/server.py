from settings import config
from application import create_app
from flask_cors import CORS
from utils.helper import get_os
from threading import Thread
from service.mq_consumer.mq_consumer_service import MQConsumerService

# Framework
# run on windows/visual studio server.py use dev
# run on docker use production (docker uses linux)
c = None
if get_os() == 'Windows':
    c=config['development']
elif get_os() == "Linux":
    c=config['production']

app = create_app(c)
CORS(app,origins='*')


def start_consumer():
    host = app.config['RABBITMQ_HOST']
    queue_name = app.config['RABBITMQ_QUEUE']
    consumer = MQConsumerService(host, queue_name)
    consumer.start_consuming()

def onConsumer():
    if app.config['RABBITMQ_WORKING_FLAG'] == 'Y':
        thread = Thread(target=start_consumer)
        thread.start()


if __name__ == '__main__':
    onConsumer()
    app.run(host="0.0.0.0", port=5001)
    