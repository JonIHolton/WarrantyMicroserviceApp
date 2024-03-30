from flask import Flask, request, jsonify
from datetime import datetime
import requests
import dotenv
from modules.WarrantyClaim import WarrantyClaim
import threading
import logging

app = Flask(__name__)
warranty_request_service_url = dotenv.get('WarrantyRequestURL') or "http://warranty-request-service:5000"
warranty_validation_service_url = dotenv.get('WarrantyValidationURL') or "http://warranty-validation-service:5000"

def check_validity_of_warranty(warranty_claim):
    logging.info("Checking validity of warranty")
    get_request = (
        f'{warranty_validation_service_url}/validate/{warranty_claim.getSerialNumber()}' + 
        f'(?claim_date={warranty_claim.getClaimDate()}'
    )
    response = requests.get(get_request)
    if response.status_code == 200 and response.json()["status"] == "valid":
        logging.info("Response from warranty validation service: " + response.json()["message"])
        return True
    elif response.status_code == 200 and response.json()["status"] == "expired":
        logging.info("Response from warranty validation service: " + response.json()["message"])
        return False
    else:
        logging.info("Response from warranty validation service: " + response.json()["message"])
        return False
    
def continue_process_of_data(warranty_claim):
    # invoke the warranty validation service to check the validity of the warranty
    validation_status = check_validity_of_warranty(warranty_claim)
    # invoke the warranty request service to update the status of the warranty claim
    requests.put()
    
@app.route('/warranty-claim-submission', methods=['POST'])
def submit_warranty_claim():
    logging.info("Received a warranty claim submission request")
    # Extract the serial number, claim date, email, and picture of receipt from the request
    serial_number = request.json['serial_number']
    claim_date = request.json['claim_date']
    email = request.json['email']
    picture_of_receipt = request.json['picture_of_receipt']
    warranty_claim = WarrantyClaim(serial_number, claim_date, email, picture_of_receipt)
    
    # Invoke warranty request service to create a warranty record
    response = requests.post(f'{warranty_request_service_url}/submit-claim', json=request.json)
    
    # An error occurred while creating the warranty claim
    if response.status_code != 201:
        logging.info("Error occured while creating claim: " + response.json()["message"])
        return jsonify({"message": response.json()["message"], "status": "error"}), 400
    
    # Start a new thread to handle logic after returning the response
    thread = threading.Thread(target=continue_process_of_data, args=(warranty_claim,))
    thread.start()
    
    # Return a success response
    return jsonify({"message": "Claim submitted successfully", "status": "success"}), 200