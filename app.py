import email
import re
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask import abort
from flask import jsonify
from db_config import DB_CONFIG
import datetime
import jwt 
app = Flask(__name__)
ma = Marshmallow(app)



app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
CORS(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

SECRET_KEY = "b'|\xe7\xbfU3`\xc4\xec\xa7\xa9zf:}\xb5\xc7\xb9\x139^3@Dv'"


from model.models import *
from model.schemas import * 

user_schema = UserSchema()

def create_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=4),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm='HS256'
    )


def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None


def decode_token(token):
    payload = jwt.decode(token, SECRET_KEY, 'HS256')
    return payload['sub']


@app.route('/signin',methods = ['GET'])
def render_sign_in():
    return render_template('sign_in.html')

@app.route('/signin',methods = ['POST'])
def sign_in():
    user_name = (request.form['user_email'])
    password = (request.form['user_password'])
    user_instance = User.query.filter_by(user_name=user_name).first()
    if user_instance is None:
        return render_sign_in()
    
    if not bcrypt.check_password_hash(user_instance.hashed_password, password):
        return render_sign_in()
    return render_template('page2.html')
    # return render_sign_in()
        
@app.route('/signup',methods = ['GET'])
def render_sign_up():
    return render_template('sign_up.html')


@app.route('/signup',methods = ['POST'])
def sign_up():
    user_name = request.form["user_name"]
    password = request.form["password"]
    user_email = request.form['email']
    confirm_pass = request.form['confirm_password']
    nationality = request.form['nationality']
    if(password != confirm_pass):
        abort(403)
    user_instance = User.query.filter_by(user_name = user_name).first()
    if(user_instance != None):
        abort(403)
    user_instance = User(user_name, password,email=user_email,nationality=nationality)
    db.session.add(user_instance)
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/Homepage',methods =["GET"])
def home_page():
    return render_template('page2.html')


