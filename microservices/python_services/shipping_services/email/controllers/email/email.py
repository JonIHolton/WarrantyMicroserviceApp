from flask import Flask, request, jsonify, current_app
from service.email.email_service import EmailService

from . import api_email

@api_email.route('/send', methods=['POST'])
def send_email():
    data = request.json
    subject = data.get('subject')
    sender = data.get('sender')  
    recipients = data.get('recipients') 
    name = data.get('name')
    email = data.get('email')
    signup_date = data.get('signup_date')

    if not all([subject, sender, recipients,name, email,signup_date]):
        return jsonify({'error': 'Missing required parameters'}), 400

    email_service = EmailService(
        current_app.config['MAIL_SERVER'],
        current_app.config['MAIL_PORT'],
        current_app.config['MAIL_USERNAME'],
        current_app.config['MAIL_PASSWORD']
    )

    email_service.send_email(subject, sender, recipients,name, email,signup_date)

    # email_service.send_email(
    #     subject="Welcome to Flask Mail Service",
    #     sender="noreply@example.com",
    #     recipients=["user@example.com"],
    #     name="John Doe",
    #     email="user@example.com",
    #     signup_date="January 1, 2020"
    # )

    return jsonify({'message': 'Email sent successfully'}), 200