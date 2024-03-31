from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace these with the actual API details of the 3rd Party Payment Provider
PAYMENT_PROVIDER_URL = 'https://api.paymentprovider.com'
API_KEY = 'your_api_key'

@app.route('/process_payment', methods=['POST'])
def process_payment():
    payment_data = request.json
    response = requests.post(
        f"{PAYMENT_PROVIDER_URL}/payments",
        json=payment_data,
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    # Handle the response from the payment provider
    if response.status_code == 200:
        return jsonify({'status': 'success', 'data': response.json()}), 200
    else:
        # Log error, handle exceptions, etc.
        return jsonify({'status': 'error', 'message': response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
