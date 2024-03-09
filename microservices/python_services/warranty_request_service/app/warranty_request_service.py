from flask import Flask, request, jsonify
from pymongo import MongoClient
import pika
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# MongoDB setup
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client[os.getenv("MONGO_DB_NAME")]
claims_collection = db[os.getenv("MONGO_COLLECTION_NAME")]

# RabbitMQ setup
rabbitmq_connection = pika.BlockingConnection(pika.URLParameters(os.getenv("RABBITMQ_URI")))
rabbitmq_channel = rabbitmq_connection.channel()
rabbitmq_channel.queue_declare(queue=os.getenv("RABBITMQ_QUEUE_NAME"))

@app.route('/submit-claim', methods=['POST'])
def submit_claim():
    # Extract claim details from the form
    claim_data = request.form.to_dict()
    # Store the claim in MongoDB
    claim_id = claims_collection.insert_one(claim_data).inserted_id
    # Publish a message to RabbitMQ
    rabbitmq_channel.basic_publish(
        exchange='',
        routing_key=os.getenv("RABBITMQ_QUEUE_NAME"),
        body=str(claim_id)
    )
    return jsonify({"message": "Claim submitted successfully", "claim_id": str(claim_id)}), 200

if __name__ == '__main__':
    app.run(debug=True)
