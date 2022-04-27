from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from db_config import DB_CONFIG
import datetime

app = Flask(__name__)
ma = Marshmallow(app)



app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
CORS(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from models.models import *




@app.route('/home',methods = ['GET'])
def hello_word():
    return 'hello world'