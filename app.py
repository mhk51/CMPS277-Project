from flask import Flask, render_template, request
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
    user_email = (request.form['user_email'])
    password = (request.form['user_password'])
    if(password == 'whatever'):
        return render_template('page2.html')
    else:
        return render_sign_in()



@app.route('/user', methods=['POST'])
def user():
    user_name = request.json["user_name"]
    password = request.json["password"]
    user_instance = User(user_name, password)
    db.session.add(user_instance)
    db.session.commit()
    return jsonify(user_schema.dump(user_instance))


@app.route('/authentication', methods=['POST'])
def authentication():
    user_name = request.json["user_name"]
    password = request.json["password"]
    if user_name is None or password is None or user_name is "" or password is "":
        abort(400)
    user_instance = User.query.filter_by(user_name=user_name).first()
    if user_instance is None:
        abort(403)
    if not bcrypt.check_password_hash(user_instance.hashed_password, password):
        abort(403)
    tkn = create_token(user_instance.id)
    return jsonify(token=tkn)