from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Assuming you're using SQLite for simplicity
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warranty.db'
db = SQLAlchemy(app)

# Define a Warranty Claim model
class WarrantyClaim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), nullable=False)
    customer_id = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Open') # Possible statuses: Open, Processing, Closed

# Endpoint to create a warranty claim
@app.route('/warranty_claims', methods=['POST'])
def create_warranty_claim():
    data = request.json
    claim = WarrantyClaim(product_id=data['product_id'], customer_id=data['customer_id'])
    db.session.add(claim)
    db.session.commit()
    return jsonify({'message': 'Warranty claim created', 'claim_id': claim.id}), 201

# Endpoint to get the status of a warranty claim
@app.route('/warranty_claims/<int:claim_id>', methods=['GET'])
def get_warranty_claim(claim_id):
    claim = WarrantyClaim.query.get_or_404(claim_id)
    return jsonify({'product_id': claim.product_id, 'status': claim.status}), 200

# Endpoint to close a warranty claim
@app.route('/warranty_claims/<int:claim_id>/close', methods=['PUT'])
def close_warranty_claim(claim_id):
    claim = WarrantyClaim.query.get_or
