from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/book'
#dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #without this, every change is tracked

db = SQLAlchemy(app) #initialise a connection to the database

@app.route("/apply",methods=['GET', 'POST'])  
def apply():
    return render_template("apply.html")

@app.route("/label",methods=['GET', 'POST'])
def label():
    return render_template("label.html")

@app.route("/alternative",methods=['GET', 'POST'])
def alternative():
    return render_template("alternative.html")
    
@app.route("/requeststatus",methods=['GET', 'POST'])
def request():
    return render_template("request.html")

if __name__ == "__main__":
    app.run(port = 5002, debug = True)
