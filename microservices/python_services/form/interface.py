from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/book'
#dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #without this, every change is tracked

db = SQLAlchemy(app) #initialise a connection to the database

@app.route("/apply",methods=['GET', 'POST'])  
def apply():
    if request.method == "POST":
        return render_template("apply.html")
    else:
        return render_template("apply.html")

@app.route("/label",methods=['GET', 'POST'])
def label():
    return render_template("label.html")

@app.route("/alternative",methods=['GET', 'POST'])
def alternative():
    if request.method == "POST":
        result = request.form['cNum']
        return render_template("alternative.html", result = result)
    else:
        return render_template("alternative.html")
    
@app.route("/alternative/<string:caseNum>")
def getCase(caseNum):
    # book = db.session.scalars(
    # 	db.select(Book).filter_by(isbn13=isbn13).
    # 	limit(1)
    #     ).first()

    # if book:
    #     return jsonify(
    #         {
    #             "code": 200,
    #             "data": book.json()
    #         }
    #     )
    # return jsonify(
    #     {
    #         "code": 404,
    #         "message": "Book not found."
    #     }
    # ), 404
    return render_template("apply.html")

if __name__ == "__main__":
    app.run(port = 5000, debug = True)
