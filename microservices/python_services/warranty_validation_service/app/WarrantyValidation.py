from flask import Flask
from flask import request
from DAO.WarrantyDAO import WarrantyDAO
from datetime import datetime
from flask import jsonify


app = Flask(__name__)
warrantyDAO = WarrantyDAO()

@app.route('/validate/<serial_number>')
def validate(serial_number):
    warranty = warrantyDAO.get_warranty(serial_number)
    # claim_timestamp is a timestamp in the format YYYY-MM-DD
    claim_date = datetime.strptime(request.args.get('claim_timestamp'), '%Y-%m-%d').date()
    if warranty:
        if warranty.isValid(claim_date):
            # Warranty is valid
            return jsonify({"message": "Valid warranty", "status": "valid"}), 200
        else:
            # Warranty exists but is expired
            return jsonify({"message": "Expired warranty", "status": "expired"}), 200
    else:
        # Serial number is invalid or warranty does not exist
        return jsonify({"message": "Invalid serial number", "status": "error"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)