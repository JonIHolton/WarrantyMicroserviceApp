import enum
import logging
import amqp_connection
import requests
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import pika

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

connection = amqp_connection.create_connection()
channel = connection.channel()
exchangename = "warranty_service" # exchange name 
exchangetype="topic"

# Healthcheck
@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    app.logger.info("Healthcheck endpoint reached.")
    return jsonify({"code": 200, "message": "Purchase resale ticket service is running!"})


def check_inventory_for_identical_replacement(model_Id):
    inventory_service_url = f"http://inventory-service:5002/api/inventory/model2/{model_Id}"
    app.logger.info(f"Checking inventory for model ID: {model_Id}")

    try:
        response = requests.get(inventory_service_url)
        if response.status_code == 200:
            inventory_count = response.json().get('data', {}).get('InventoryCount', 0)
            app.logger.info(f"Inventory count for model ID {model_Id}: {inventory_count}")
            return {"available": True, "count": inventory_count} if inventory_count > 0 else {"available": False, "count": 0}
        app.logger.error(f"Received non-200 status code: {response.status_code}")
        return {"available": False, "error": f"Received status code {response.status_code}"}
    except Exception as e:
        app.logger.error(f"An error occurred while checking inventory: {str(e)}")
        return {"available": False, "error": "Exception occurred during inventory check"}




def check_inventory_for_alternative(model_type, model_Id): 
    inventory_service_url = f"http://inventory-service:5002/api/inventory/models"

    
    
    try:
        # Make the GET request to fetch all GPUs
        response = requests.get(inventory_service_url)
        
        # Ensure the request was successful
        if response.status_code == 200:
            
            # Parse the JSON response
            gpus = response.json().get('data', [])

        
            cleaned_model_type = model_type.strip('"')  # Removes the quotation marks
            integer_model_type = int(cleaned_model_type)  # Converts the cleaned string to an integer

            
        # Search for the first GPU that matches the given model_type
            for gpu in gpus:
             
                if (int(gpu.get('model_Type')) == integer_model_type) and (gpu.get('ModelName').strip() != model_Id.strip()):
                    # Return the model_Id of the matching GPU
                    
                    return gpu.get('ModelName')
            # If no matching model_type is found
            return "no alternative"
        else:
            
            app.logger.info(f"Failed to retrieve GPUs. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    

def offer_alternative(request_Id, model_Id, claimee, email) :

    message = {
        "request_Id" : request_Id,
        "model_Id" : model_Id,
        "claimee" : claimee,
        "email" : email
    } 

    

    message = json.dumps(message)

    channel.basic_publish(exchange=exchangename, routing_key="offer.alternative",  
    body=message, properties=pika.BasicProperties(delivery_mode = 2))



import requests
import json

def update_request_status(status, requestId, claimee, email):
    # Define the URL for the PATCH request
    warranty_request_service_url = f"http://warranty-request-service:8080/requests/{requestId}/status"
    
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
            app.logger.info(f"Status for requestId: {requestId} updated to {status}.")
            return True
        else:
            # If the response includes a JSON message, attempt to decode it
            try:
                error_message = response.json().get('message', 'No additional information')
            except ValueError:
                # If no JSON message, use the raw text response
                error_message = response.text
            app.logger.info(f"Status for requestId: {requestId} failed to update. Response: {error_message}")
            return False
    except requests.exceptions.RequestException as e:
        app.logger.info(f"An error occurred while updating request status: {e}")
        return False




@app.route('/requests/<requestId>/status/notRepairable', methods=['POST'])
def handle_replacement_request(requestId):
    app.logger.info("Replacement request endpoint reached.")

    # Extract the status from the request's JSON body
    # data = request.json
    # status = data.get('status')

    # Extract claimee and email from the request's headers
    claimee = request.headers.get('claimee')
    email = request.headers.get('email')
    model_Id = request.headers.get('modelId')
    model_Type= request.headers.get('modelType')
    
    app.logger.info(request.headers)
    app.logger.info(f"claimee: {claimee}")
    app.logger.info(f"email: {email}")
    app.logger.info(f"model_Id: {model_Id}")
    app.logger.info(f"model_Type: {model_Type}")

    # alternative_status = check_inventory_for_alternative(model_Type, model_Id)

    # return alternative_status

   
    # checks inventory service for a 1:1 replacement
    replacement_status = check_inventory_for_identical_replacement(model_Id)

    

    # if have
    if replacement_status["available"] == True:

        status = 'not_repairable_one_to_one_replacement'
        update_request_status(status, requestId, claimee, email) 
        
        return {"status": "success", "message": "Replacement request successfully processed."}
    
    # no 1:1 replacement
    else :
    
        # check for alternative
         alternative_status = check_inventory_for_alternative(model_Type, model_Id)
        
         if alternative_status != "no alternative" :

            
            offer_alternative(requestId, model_Id, claimee, email) 
            return {"status": "success", "message": "Alternative replacement offered."}
         
         # no alternative 
         else :
             
             status = 'pending_alternative_refund'
             update_request_status(status, requestId, claimee, email) 
            
             return {"status": "success", "message": "No alternative replacement available. Refund pending."}
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)