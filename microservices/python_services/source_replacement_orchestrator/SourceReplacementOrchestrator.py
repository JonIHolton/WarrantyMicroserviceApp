import enum
import logging

import requests
from flask import Flask, request, jsonify, Response
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# Healthcheck
@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    app.logger.info("Healthcheck endpoint reached.")
    return jsonify({"code": 200, "message": "Purchase resale ticket service is running!"})


def check_inventory_for_identical_replacement(model,caseId):
    inventory_service_url = f"http://inventory-management-service/{caseId}check-replacement"
    
    # Append the model as a query parameter
    params = {'model': model}
    
    try:
        response = requests.get(inventory_service_url, params=params)
        
        # Assuming the service returns a JSON response with a field that indicates success or failure
        if response.status_code == 200 and response.json().get('status') == 'success':
            app.logger.info(f"Replacement found for model {model}.")
            return True
        else:
            app.logger.info(f"No replacement available for model {model}. Response: {response.json().get('message', 'No additional information')}")
            return False
    except requests.exceptions.RequestException as e:
        # Handle exceptions related to the request itself, such as network errors.
        app.logger.info(f"An error occurred while checking inventory: {e}")
        return False



def check_inventory_for_alternative(model_type, caseId): 
    inventory_service_url = f"http://inventory-management-service/{caseId}check-alternative"
    
    # Append the model as a query parameter
    params = {'model_type': model_type}
    
    try:
        response = requests.get(inventory_service_url, params=params)
        
        # Assuming the service returns a JSON response with a field that indicates success or failure
        if response.status_code == 200 and response.json().get('status') == 'success':
            app.logger.info(f"Alternative found for model {model_type}.")
            return True
        else:
            app.logger.info(f"No replacement available for model {model_type}. Response: {response.json().get('message', 'No additional information')}")
            return False
    except requests.exceptions.RequestException as e:
        # Handle exceptions related to the request itself, such as network errors.
        app.logger.info(f"An error occurred while checking inventory: {e}")
        return False


def update_request_status(request_status,caseId) :
    warranty_request_service_url = f"http://warranty-request-service/{caseId}/update-status"

    params = {'request_status': request_status}
    try:
        response = requests.post(warranty_request_service_url, params=params)
        
        # Assuming the service returns a JSON response with a field that indicates success or failure
        if response.status_code == 200 and response.json().get('status') == 'success':
            app.logger.info(f"Status for CaseId: {caseId} updated to {request_status}.")
            return True
        else:
            app.logger.info(f"Status for CaseId: {caseId} failed to update to {request_status}. Response: {response.json().get('message', 'No additional information')}")
            return False
    except requests.exceptions.RequestException as e:
        # Handle exceptions related to the request itself, such as network errors.
        app.logger.info(f"An error occurred while updating request status: {e}")
        return False


@app.route('/requests/<caseId>/status/notRepairable', methods=['POST'])
def handle_replacement_request(caseId):
    app.logger.info("Replacement listing endpoint reached.")

    
    data = request.json
    request_status = data.get('status')
    model = data.get('model')
    model_type = data.get('model_type')

    replacement_status = check_inventory_for_identical_replacement(model, caseId)

    if replacement_status == 200 :
        request_status = 'replacement available'
        update_request_status(request_status, caseId) 
        return jsonify
    
    else :

         replacement_status = check_inventory_for_alternative(model_type, caseId)

         if replacement_status == 200 :
            request_status = 'alternative available'
            update_request_status(request_status, caseId) 
            return jsonify
        


if __name__ == '__main__':
    app.run(debug=True, port=5000)





