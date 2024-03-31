from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/refund_records'
#dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Refund(db.Model):
    __tablename__ = 'refund_records'
    RequestID = db.Column(db.Integer(), primary_key=True)
    RefundAmt = db.Column(db.Float(precision=2), nullable=False)
    RefundDateTime = db.Column(db.String(64), nullable=False)

    def __init__(self, RequestID, RefundAmt, RefundDateTime):
        self.RequestID = RequestID
        self.RefundAmt = RefundAmt
        self.RefundDateTime = RefundDateTime

    def json(self):
        return {"RequestID": self.RequestID, "RefundAmt": self.RefundAmt, "RefundDateTime": self.RefundDateTime}

@app.route("/refund_records")
def get_all():
    refund_list = db.session.scalars(db.select(Refund)).all()

    if len(refund_list):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "refund_records": [refund.json() for refund in refund_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no records."
        }
    ), 404

@app.route("/refund_records/<int:RequestID>")
def find_by_requestid(RequestID):
    refund = db.session.scalars(
    	db.select(Refund).filter_by(RequestID=RequestID).
    	limit(1)
        ).first()

    if refund:
        return jsonify(
            {
                "code": 200,
                "data": refund.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Record not found."
        }
    ), 404


@app.route("/refund_records/<int:RequestID>",methods=["POST"])
def create_refund_record(RequestID):
    if (db.session.scalars(
      db.select(Refund).filter_by(RequestID=RequestID).
      limit(1)
      ).first()
      ):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "RequestID": RequestID
                },
                "message": "Item has already been refunded."
            }
        ), 400

    data = request.get_json()
    refund = Refund(RequestID, **data)

    try:
        db.session.add(refund)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "RequestID": RequestID
                },
                "message": "An error occurred creating the record."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": refund.json()
        }
    ), 201

if __name__ == "__main__":
    app.run(port = 5000, debug = True)
