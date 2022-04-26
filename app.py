from __future__ import unicode_literals
from xmlrpc.client import DateTime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import datetime


app = Flask(__name__)
ma = Marshmallow(app)

DB_CONFIG = 'mysql+pymysql://root:12345@localhost:3306/cloudgaming'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
CORS(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)




class User(db.Model):
    user_name = db.Column(db.String(30), primary_key=True,unique = True)
    hashed_password = db.Column(db.String(128))
    cart_balance = db.Column(db.Float)
    year_of_registration = db.Column(db.DateTime)
    nationality = db.Column(db.String(30))
    email = db.Column(db.String(30),unique = True)
    community_Name = db.Column(db.String(30))
    # server_Name = db.Column()
    # server_Region = db.Column()

    def __init__(self, user_name, password,nationality,email):
        super(User, self).__init__(user_name=user_name)
        self.hashed_password = bcrypt.generate_password_hash(password)
        self.cart_balance = 0.0
        self.year_of_registration = datetime.datetime.now()
        self.nationality = nationality
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name")
        model = User



@app.route('/home',methods = ['GET'])
def hello_word():
    return 'hello world'