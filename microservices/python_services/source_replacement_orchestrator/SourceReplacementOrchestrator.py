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


def check_inventory_for_identical_replacement(model_Id):
    inventory_service_url = f"http://localhost:5000/model/{model_Id}"
    
    
    try:
        response = requests.get(inventory_service_url)
        
         # Check if the request was successful
        if response.status_code == 200:
            # Extract the InventoryCount field from the JSON response
            inventory_count = response.json().get('data', {}).get('InventoryCount', 0)
            
            # Check if InventoryCount is greater than 0
            return inventory_count > 0
        else:
            # Handle responses other than 200 OK
            print(f"Error: Received status code {response.status_code}")
            return False
    except Exception as e:
        # Handle exceptions such as network errors
        print(f"An error occurred: {str(e)}")
        return False



def check_inventory_for_alternative(model_type, requestId): 
    inventory_service_url = f"http://inventory-management-service/{requestId}check-alternative"
    
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


import requests
import json

def update_request_status(status, requestId, claimee, email):
    # Define the URL for the PATCH request
    warranty_request_service_url = f"http://localhost:8080/requests/{requestId}/status"
    
    # Set the headers including 'Content-Type', 'claimee', and 'email'
    headers = {
        'Content-Type': 'text/plain',  # Since we're sending a plain string
        'claimee': claimee,
        'email': email
    }
    
    try:
        # Send the PATCH request with the plain string in the body
        # No need to use json.dumps since we're sending a plain string
        response = requests.patch(warranty_request_service_url, data=status, headers=headers)
        
        # Check if the response status code indicates success (200 OK)
        if response.status_code == 200:
            print(f"Status for requestId: {requestId} updated to {status}.")
            return True
        else:
            # If the response includes a JSON message, attempt to decode it
            try:
                error_message = response.json().get('message', 'No additional information')
            except ValueError:
                # If no JSON message, use the raw text response
                error_message = response.text
            print(f"Status for requestId: {requestId} failed to update. Response: {error_message}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while updating request status: {e}")
        return False




@app.route('/requests/<requestId>/status/notRepairable', methods=['POST'])
def handle_replacement_request(requestId):
    app.logger.info("Replacement request endpoint reached.")

    # Extract the status from the request's JSON body
    data = request.json
    status = data.get('status')

    # Extract claimee and email from the request's headers
    claimee = request.headers.get('claimee')
    email = request.headers.get('email')
    model_Id = request.headers.get('model_Id')
    model_Type= request.headers.get('model_Type')

    # # Check if required information is present
    # if not status or not claimee or not email:
    #     return jsonify({"error": "Missing required fields"}), 400
    

    # checks inventory service for a 1:1 replacement
    replacement_status = check_inventory_for_identical_replacement(model_Id)

    # if have
    if replacement_status :
        status = 'not_repairable_one_to_one_replacement'
        update_request_status(status, requestId, claimee, email) 
        return jsonify
    
    # no 1:1 replacement
    else :
        return 

    #     # check for alternative
    #      alternative_status = check_inventory_for_alternative(model_Type)
        
    #      if alternative_status :

            
    #         request_status = 'pending_alternative'
    #         update_request_status(request_status, requestId) 
    #         return jsonify
         
    #      # no alternative 
    #      else :
             
    #          request_status = 'pending_refund'
    #          update_request_status(request_status, requestId) 
    #          return jsonify

         

    # # Attempt to update the request status
    # success = update_request_status(status, requestId, claimee, email)

    # # Return an appropriate response based on the outcome
    # if success:
    #     return jsonify({"message": "Request status updated successfully"}), 200
    # else:
    #     return jsonify({"error": "Failed to update request status"}), 500


    # replacement_status = check_inventory_for_identical_replacement(model, requestId)

    # if replacement_status == 200 :
    #     request_status = 'replacement available'
    #     update_request_status(request_status, requestId) 
    #     return jsonify
    
    # else :

    #      replacement_status = check_inventory_for_alternative(model_type, requestId)

    #      if replacement_status == 200 :
    #         request_status = 'alternative available'
    #         update_request_status(request_status, requestId) 
    #         return jsonify
        


if __name__ == '__main__':
    app.run(debug=True, port=5000)





