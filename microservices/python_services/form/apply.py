from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/book'
#dialect+driver://username:password@host:port/database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #without this, every change is tracked

db = SQLAlchemy(app) #initialise a connection to the database

@app.route("/apply",methods=['GET', 'POST'])  
def index():
    return render_template("index.html", image_file="images/image1.png")

if __name__ == "__main__":
    app.run(port = 5000, debug = True)
