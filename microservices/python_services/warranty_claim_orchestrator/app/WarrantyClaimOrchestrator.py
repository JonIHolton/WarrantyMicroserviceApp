from flask import Flask, request, jsonify
from datetime import datetime, date
import requests
import os
import logging

from modules.WarrantyClaim import WarrantyClaim

app = Flask(__name__)
warranty_request_service_url = os.getenv("WARRANTY_REQUEST_SERVICE") or "http://warranty-request-service:5000"
warranty_validation_service_url = os.getenv("WARRANTY_VALIDATION_SERVICE") or "http://warranty-validation-service:5000"

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def check_validity_of_warranty(warranty_claim : WarrantyClaim):
    get_request = (
        f'{warranty_validation_service_url}/validate/{warranty_claim.getSerialNumber()}'
        + f'?claim_date={warranty_claim.getClaimDate()}'
    )
    response = requests.get(get_request)
    if response.status_code == 200 and response.json()["status"] == "valid":
        logging.debug("Response from warranty validation service: " + response.json()["message"])
        return True
    elif response.status_code == 400 and response.json()["status"] == "expired":
        logging.debug("Response from warranty validation service: " + response.json()["message"])
        return False
    else:
        logging.debug("Response from warranty validation service: " + response.json()["message"])
        return False
    
@app.route('/warranty-claim-submission', methods=['POST'])
def submit_warranty_claim():
    logging.debug(f"Received a warranty claim submission request: {request.json}")
    
    serial_number = request.json['serial_number']
    claim_date : date = datetime.strptime(request.json['claim_date'], '%Y-%m-%d').date()
    email = request.json['email']
    picture_of_receipt = request.json['picture_of_receipt']
    warranty_claim = WarrantyClaim(serial_number, claim_date, email, picture_of_receipt)

    # Invoke warranty request service to create a warranty record
    logging.debug("Creating warranty claim")
    # response = requests.post(f'{warranty_request_service_url}/submit-claim', json=request.json)
    # logging.debug("Response from warranty request service: " + response.json["message"])
    
    # An error occurred while creating the warranty claim
    # if response.status_code != 201:
    #     logging.debug("Error occured while creating claim: " + response.json()["message"])
    #     return jsonify({"message": response.json()["message"], "status": "error"}), 400
    
    # Invoke the warranty validation service to check the validity of the warranty
    logging.debug("Checking validity of warranty")
    validation_status : bool = check_validity_of_warranty(warranty_claim)
    logging.debug(f"Warranty validation status: {validation_status}")
    
    # Invoke the warranty request service to update the status of the warranty claim
    logging.debug("Updating warranty claim status")
    # response = requests.post(
    #     f'{warranty_request_service_url}/update-claim-status', 
    #         json={"serial_number": serial_number, "status": "pending"}
    # )
    # logging.debug("Response from warranty request service: " + response.json()["message"])
    
    # Return a success response
    return jsonify({"message": "Claim submitted successfully", "status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)