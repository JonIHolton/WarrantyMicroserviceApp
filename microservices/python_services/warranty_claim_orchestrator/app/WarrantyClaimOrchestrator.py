from flask import Flask, request, jsonify
from datetime import datetime, date
import requests
import os
import logging
from flask_cors import CORS

from modules.WarrantyClaim import WarrantyClaim

app = Flask(__name__)
CORS(app)
warranty_request_service_url = os.getenv("WARRANTY_REQUEST_SERVICE") or "http://warranty-request-service:8080/requests"
warranty_validation_service_url = os.getenv("WARRANTY_VALIDATION_SERVICE") or "http://warranty-validation-service:5000"

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def check_validity_of_warranty(warranty_claim : WarrantyClaim):
    get_request = (
        f'{warranty_validation_service_url}/validate/{warranty_claim.getUnitId()}'
        + f'?claim_date={datetime.today().strftime("%Y-%m-%d")}'
    )
    try:
        response = requests.get(get_request)
        if response.status_code == 200 and response.json()["status"] == "valid":
            return "valid"
        elif response.status_code == 400 and response.json()["status"] == "expired":
            return "expired"
        else:
            return "invalid_serial_no"
    except Exception as e:
        logging.debug("Error occured while validating warranty: " + str(e))
        return "invalid_serial_no"

def create_warranty_request(warranty_claim : WarrantyClaim):
    '''
    post request
    send to localhost:8080/request
    {
        "unit_Id": "U12345",
        "model_Id": "M12345",
        "model_Type": "Electronics",
        "claimee": "John Doe",
        "email": "johndoe@example.com",
        "description": "Request to recycle an old electronic device."
    }
    The return is a string: Request added with ID: 8
    '''
    try: 
        json_payload = {
            "unit_Id": warranty_claim.getUnitId(),
            "model_Id": warranty_claim.getModelId(),
            "model_Type": warranty_claim.getModelType(),
            "claimee": warranty_claim.getClaimee(),
            "email": warranty_claim.getEmail(),
            "description": warranty_claim.getDescription()
        }
        response = requests.post(warranty_request_service_url, json=json_payload)
        if response.status_code == 201 or response.status_code == 200:
            return response.text
        else:
            logging.debug("Error occured while creating claim request: " + response.json()["message"])
            return None
    except Exception as e:
        logging.debug("Error occured while creating claim request: " + str(e))
        return None
            

def update_request_status(request_status, requestId, claimee, email):
    '''
    request_status = "valid" or "expired" or "invalid_serial_no"
    '''
    # Define the URL for the PATCH request
    warranty_request_update_service_url = f"{warranty_request_service_url}/{requestId}/status"
    
    # Set the headers including 'Content-Type', 'claimee', and 'email'
    headers = {
        'Content-Type': 'text/plain',  # Since we're sending a plain string
        'claimee': claimee,
        'email': email
    }
    
    try:
        # Send the PATCH request with the plain string in the body
        # No need to use json.dumps since we're sending a plain string
        response = requests.patch(warranty_request_update_service_url, data=request_status, headers=headers)
        
        # Check if the response status code indicates success (200 OK)
        if response.status_code == 200:
            logging.debug(f"Status for requestId: {requestId} updated to {request_status}.")
            return True
        else:
            # If the response includes a JSON message, attempt to decode it
            try:
                error_message = response.json().get('message', 'No additional information')
            except ValueError:
                # If no JSON message, use the raw text response
                error_message = response.text
            logging.debug(f"Status for requestId: {requestId} failed to update. Response: {error_message}")
            return False
    except requests.exceptions.RequestException as e:
        logging.debug(f"An error occurred while updating request status: {e}")
        return False
    
@app.route('/warranty-claim-submission', methods=['POST'])
def submit_warranty_claim():
    '''
    Expected JSON format:
    {
        unit_id: "U12345",
        model_id: "M12345",
        model_type: "Electronics",
        claimee: "John Doe",
        email: "test@example.com",
        description: "Request to recycle an old electronic device."
    }
    '''
    logging.debug(f"Received a warranty claim submission request: {request.json}")
    # Validate the JSON request
    if not all(key in request.json for key in ['unit_id', 'model_id', 'model_type', 'claimee', 'email', 'description']):
        return jsonify({"message": "Missing required fields", "status": "error"}), 400
    
    unit_id = request.json['unit_id']
    model_id = request.json['model_id']
    model_type = request.json['model_type']
    claimee = request.json['claimee']
    email = request.json['email']
    description = request.json['description']
    warranty_claim = WarrantyClaim(unit_id, model_id, model_type, claimee, email, description)
    logging.debug(f"Warranty claim object created: {warranty_claim}")

    # Invoke warranty request service to create a warranty record
    logging.debug("Creating warranty claim")
    response = create_warranty_request(warranty_claim)
    if response is None:
        return jsonify({"message": "Error occured while creating claim", "status": "error"}), 400
    
    logging.debug("Response from warranty request service: " + response)
    
    # Extract the requestId from the response
    requestId = response.split()[-1]
    
    # Invoke the warranty validation service to check the validity of the warranty
    logging.debug("Checking validity of warranty")
    validation_status : str = check_validity_of_warranty(warranty_claim)
    logging.debug(f"Warranty validation status: {validation_status}")
    
    # Invoke the warranty request service to update the status of the warranty claim
    logging.debug("Updating warranty claim status")
    response = update_request_status(validation_status, requestId, claimee, email)
    logging.debug("Response from warranty request service: " + str(response))
    
    # Return a success response
    return jsonify({"message": "Claim submitted successfully", "status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)