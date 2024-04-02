from flask import Flask, request, jsonify, current_app
from service.email.email_service import EmailService

from . import api_email

@api_email.route('/send-email', methods=['POST'])
def send_email():
    try:
        # Extracting email data from request body
        data = request.get_json()
        recipient = data['recipient']
        subject = data['subject']
        text_body = data.get('text_body', '')  # Defaulting to empty string if not provided
        html_body = data.get('html_body', '')  # Defaulting to empty string if not provided

        # Sending the email
        EmailService.send_email_via_postmark(recipient, subject, text_body, html_body)

        # Returning success response
        return jsonify({'status': 'success', 'message': 'Email sent successfully'}), 200
    except KeyError as e:
        # Handling missing data error
        return jsonify({'status': 'error', 'message': f'Missing data: {e}'}), 400
    except Exception as e:
        # Handling general error
        return jsonify({'status': 'error', 'message': f'An error occurred: {e}'}), 500