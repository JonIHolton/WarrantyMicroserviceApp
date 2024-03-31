from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace the user, password, host, port, and database with your actual MySQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@host:port/FinancialRecordsDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class RefundRecord(db.Model):
    __tablename__ = 'RefundRecords'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('initiated', 'processed', 'completed'), nullable=False)

    def __init__(self, transaction_id, amount, status):
        self.transaction_id = transaction_id
        self.amount = amount
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'amount': str(self.amount),
            'status': self.status
        }

@app.route('/financial_records', methods=['POST'])
def create_financial_record():
    data = request.json
    new_record = RefundRecord(
        transaction_id=data['transaction_id'],
        amount=data['amount'],
        status=data['status']
    )
    db.session.add(new_record)
    db.session.commit()
    return jsonify(new_record.to_dict()), 201

@app.route('/financial_records/<int:record_id>', methods=['GET'])
def get_financial_record(record_id):
    record = RefundRecord.query.get_or_404(record_id)
    return jsonify(record.to_dict())

if __name__ == '__main__':
    db.create_all()  # Create tables based on the models if not already existing
    app.run(debug=True)


