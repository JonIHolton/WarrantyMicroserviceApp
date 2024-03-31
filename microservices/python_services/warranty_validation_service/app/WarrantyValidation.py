from flask import Flask
from flask import request
from DAO.WarrantyDAO import WarrantyDAO
from datetime import datetime
from flask import jsonify
import logging

app = Flask(__name__)
warrantyDAO = WarrantyDAO()

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@app.route('/validate/<serial_number>')
def validate(serial_number):
    logging.debug(f"Received a warranty validation request for serial number: {serial_number}")
    warranty = warrantyDAO.get_warranty(serial_number)
    # claim_timestamp is a timestamp in the format YYYY-MM-DD
    claim_date = datetime.strptime(request.args.get('claim_date'), '%Y-%m-%d').date()
    if warranty:
        if warranty.isValid(claim_date):
            # Warranty is valid
            logging.debug("Warranty is valid")
            return jsonify({"message": "Valid warranty", "status": "valid"}), 200
        else:
            # Warranty exists but is expired
            logging.debug("Warranty is expired")
            return jsonify({"message": "Expired warranty", "status": "expired"}), 400
    else:
        # Serial number is invalid or warranty does not exist
        logging.debug("Invalid serial number")
        return jsonify({"message": "Invalid serial number", "status": "invalid"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)