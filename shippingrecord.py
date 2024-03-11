from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/shippingrecord'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class ShippingRecord(db.Model):
    __tablename__ = 'shippingrecord'


    CaseID = db.Column(db.Integer, primary_key=True)
    ShippingInID = db.Column(db.Integer, nullable=False)
    ReceivedDateTime = db.Column(db.String(64), nullable=False)
    ShippingOutID = db.Column(db.Integer, nullable=False)
    ShippingOutDateTime = db.Column(db.String(64), nullable=False)
    Remarks = db.Column(db.String(254), nullable=False)


    def __init__(self, CaseID, ShippingInID, ReceivedDateTime, ShippingOutID, ShippingOutDateTime, Remarks):
        self.CaseID = CaseID
        self.ShippingInID = ShippingInID
        self.ReceivedDateTime = ReceivedDateTime
        self.ShippingOutID = ShippingOutID
        self.ShippingOutDateTime = ShippingOutDateTime
        self.Remarks = Remarks


    def json(self):
        return {"CaseID": self.CaseID, "ShippingInID": self.ShippingInID, "ReceivedDateTime": self.ReceivedDateTime, "ShippingOutID": self.ShippingOutID, "ShippingOutDateTime": self.ShippingOutDateTime, "Remarks" : self.Remarks}



@app.route("/shippingrecord")
def get_all():
    shippinglist = db.session.scalars(db.select(ShippingRecord)).all()


    if len(shippinglist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "shipping": [shippingrecord.json() for shippingrecord in shippinglist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no case."
        }
    ), 404


@app.route("/shippingrecord/<int:CaseID>")
def find_by_CaseID(CaseID):
    shippingrecord = db.session.scalars(
    	db.select(ShippingRecord).filter_by(CaseID=CaseID).
    	limit(1)
).first()


    if shippingrecord:
        return jsonify(
            {
                "code": 200,
                "data": shippingrecord.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Case not found."
        }
    ), 404



@app.route("/book/<int:CaseID>", methods=['POST'])
def create_shippingrecord(CaseID):
    if (db.session.scalars(
      db.select(ShippingRecord).filter_by(CaseID=CaseID).
      limit(1)
      ).first()
      ):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "CaseID": CaseID
                },
                "message": "Case already exists."
            }
        ), 400


    data = request.get_json()
    shippingrecord = ShippingRecord(CaseID, **data)


    try:
        db.session.add(shippingrecord)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "CaseID": CaseID
                },
                "message": "An error occurred creating the case."
            }
        ), 500


    return jsonify(
        {
            "code": 201,
            "data": shippingrecord.json()
        }
    ), 201



if __name__ == '__main__':
    app.run(port=5000, debug=True)