import os
import platform
import sys
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/book'
#dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #without this, every change is tracked

db = SQLAlchemy(app) #initialise a connection to the database

@app.route("/apply",methods=['GET'])  
def apply():
    return render_template("apply.html")

@app.route("/label",methods=['GET', 'POST'])
def label():
    return render_template("label.html")

@app.route("/alternative",methods=['GET', 'POST'])
def alternative():
    return render_template("alternative.html")
    
@app.route("/requeststatus",methods=['GET', 'POST'])
def request_status():
    return render_template("request.html")

@app.route("/get_all_requests", methods=["GET"])
def get_all_requests():
    api_url = "http://localhost:8080/requests/all"
    response = requests.get(api_url)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Failed to fetch ship record data'}), response.status_code
    
@app.route("/request/<int:request_Id>", methods=["PATCH"])
def update_request(request_Id):
    data = request.get_json()
    status = data['status']
    email = request.headers['email']
    claimee = request.headers['claimee']
    headers = {
        'Content-Type': 'text/plain',  # Since we're sending a plain string
        'claimee': claimee,
        'email': email
    }
    api_url = f"http://warranty-request-service:8080/requests/{request_Id}/status"
    try:
        response = requests.patch(api_url, data=status, headers=headers)
        json_response = response.json()
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid JSON response received from the remote API'}), 500
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)
        return jsonify({'status': 'error', 'message': 'Failed to communicate with place_order API: ' + ex_str}), 500

    return jsonify(json_response), response.status_code

@app.route("/request1/<int:request_Id>", methods=["POST"])
def update_request_not_repairable(request_Id):
    # data = request.get_json()
    
    app.logger.info("Interface hit")
    app.logger.info(request.headers)
    
    claimee = request.headers['claimee']
    email = request.headers['email']
    modelId = request.headers['modelId']
    modelType = request.headers['modelType']
    # data = request.get_json()  # Get JSON data from the request body
    # status = data.get('status')  # Extract 'status' from JSON data
    # Now you can use the extracted data as needed

    headers = {
        # 'Content-Type': 'application/json',
        'claimee': claimee,
        'email': email,
        'modelId': modelId,
        'modelType': modelType
    }
    
    # return headers
    
    app.logger.info(headers)
    api_url = f"http://127.0.0.1:5001/requests/{request_Id}/status/notRepairable"
    try:
        response = requests.post(api_url, data="", headers=headers)
        json_response = response.json()
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid JSON response received from the remote API'}), 500
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)
        return jsonify({'status': 'error', 'message': 'Failed to communicate with place_order API: ' + ex_str}), 500

    return jsonify(json_response), response.status_code

@app.route("/send-warranty-claim", methods=['POST'])
def send_warranty_claim():
    data = request.get_json()
    print(data)
    api_url = "http://warranty-claim-orchestrator:5000/warranty-claim-submission"
    try:
        response = requests.post(api_url, json=data)
        json_response = response.json()
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid JSON response received from the remote API'}), 500
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)
        return jsonify({'status': 'error', 'message': 'Failed to communicate with place_order API: ' + ex_str}), 500

    return jsonify(json_response), response.status_code

@app.route("/submit-label-form", methods=['POST'])
def submit_form():
    data = {
        'CaseID': request.form.get('caseNumber', ''),
        'InSerialNumber': request.form.get('serialNumber', ''),
        'InBrand': request.form.get('inBrand', ''),
        'InModel': request.form.get('inModel', ''),
        'Email': request.form.get('email', ''),
        'Remarks': request.form.get('remarks', ''),
        'ReturnAddress': request.form.get('returnAddress', '')
    }

    print(data)

    api_url = f"http://shipping-service:5001/api/shipping/shippingrecords"
    # if  get_os() == "Linux":
    #     api_url = f"http://shipping-service:5001/api/shipping/shippingrecords"

    response = requests.post(api_url, json=data)
    
    try:
        json_response = response.json()
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid JSON response received from the remote API'}), 500

    return jsonify(json_response), response.status_code


@app.route("/send-mq-email", methods=['POST'])
def send_mq_email():
    data = request.get_json()
    print(data)
    api_url = "http://shipping-service:5001/api/mq/send_message"
    # if  get_os() == "Linux":
    #     api_url = f"http://shipping-service:5001/api/mq/send_message"
    try:
        response = requests.post(api_url, json=data)
        json_response = response.json()
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid JSON response received from the remote API'}), 500
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)
        return jsonify({'status': 'error', 'message': 'Failed to communicate with place_order API: ' + ex_str}), 500

    return jsonify(json_response), response.status_code



@app.route("/getModel/<int:model_id>", methods=['GET'])
def get_model(model_id):
    api_url = f"http://inventory-service:5002/api/inventory/model/{model_id}"
    # if  get_os() == "Linux":
    #     api_url = f"http://inventory-service:5002/api/inventory/model/{model_id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Failed to fetch model data'}), response.status_code
    

@app.route("/getShippingRecord/<case_id>", methods=['GET'])
def getShippingRecord(case_id):
    api_url = f"http://shipping-service:5001/api/shipping/shippingrecords/{case_id}"
    # if  get_os() == "Linux":
    #     api_url = f"http://shipping-service:5001/api/shipping/shippingrecords/{case_id}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Failed to fetch ship record data'}), response.status_code
    
@app.route("/getShippingRecordAll", methods=['GET'])
def getShippingRecordAll():
    api_url = f"http://shipping-service:5001/api/shipping/shippingrecords/all"
    # if  get_os() == "Linux":
    #     api_url = f"http://shipping-service:5001/api/shipping//shippingrecords/all"
    response = requests.get(api_url)
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'error': 'Failed to fetch ship record data'}), response.status_code

		
@app.route("/handleInventory", methods=['POST'])
def handleInventory():
    data = request.get_json()
    print(data)
    
    model_id = data['ModelID']  
    update_data = data['data']  
    
    api_url = f"http://inventory-service:5002/api/inventory/model/{model_id}"
    # if  get_os() == "Linux":
    #     api_url = f"http://inventory-service:5002/api/inventory/model/{model_id}"
    
    try:
        response = requests.put(api_url, json=update_data)
        json_response = response.json()
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid JSON response received from the remote API'}), 500
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)
        return jsonify({'status': 'error', 'message': f'Failed to communicate with inventory API: {ex_str}'}), 500

    return jsonify(json_response), response.status_code

@app.route("/handleAlternative", methods=['POST'])
def handleAlternative():
    data = request.get_json()
    print(data)
    
    request_id = data['cNum']  
    acceptStatus = data['acceptStatus']  
    
    api_url = f"http://warranty-request-service:8080/requests/{request_id}/status"
    # if  get_os() == "Linux":
    #     api_url = f"http://inventory-service:5002/api/inventory/model/{model_id}"
    
    update_data = {
        "status": acceptStatus
    }
    
    try:
        response = requests.patch(api_url, json=update_data, headers={"claimee":"", "email": ""})
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid JSON response received from the remote API'}), 500
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)
        return jsonify({'status': 'error', 'message': f'Failed to communicate with inventory API: {ex_str}'}), 500

    return {"message": response.text}, response.status_code
    

def get_os():
    os_name = platform.system()
    if os_name == 'Windows':
        return 'Windows'
    elif os_name == 'Linux':
        return 'Linux'
    else:
        return 'Unknown'



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)


# if __name__ == "__main__":
#     app.run(port = 5002, debug = True)
