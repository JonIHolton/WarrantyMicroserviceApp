from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pika
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///refunds.db'
db = SQLAlchemy(app)

# Database model
class Refund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')

# AMQP setup for RabbitMQ
amqp_url = 'your_amqp_broker_url'
params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='email_notifications')

# Service endpoint to initiate a refund
@app.route('/initiate_refund', methods=['POST'])
def initiate_refund():
    data = request.json
    refund = Refund(transaction_id=data['transaction_id'], amount=data['amount'])
    db.session.add(refund)
    db.session.commit()
    
    # Asynchronously send an email notification
    email_data = {
        'email': data['customer_email'],
        'subject': 'Refund Initiated',
        'message': f'Your refund for transaction {refund.transaction_id} has been initiated.'
    }
    channel.basic_publish(exchange='',
                          routing_key='email_notifications',
                          body=json.dumps(email_data))
    
    return jsonify({'message': 'Refund initiated', 'refund_id': refund.id}), 200

# Service endpoint to check refund status
@app.route('/refund_status/<int:refund_id>', methods=['GET'])
def refund_status(refund_id):
    refund = Refund.query.get_or_404(refund_id)
    return jsonify({'transaction_id': refund.transaction_id, 'status': refund.status}), 200

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)
