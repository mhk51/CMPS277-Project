from flask import Flask, render_template, request
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


@app.route('/signin',methods = ['GET'])
def render_sign_in():
    return render_template('sign_in.html')

@app.route('/signin',methods = ['POST'])
def sign_in():
    user_email = (request.form['user_email'])
    password = (request.form['user_password'])
    if(password == 'whatever'):
        return render_template('page2.html')
    else:
        return render_sign_in()