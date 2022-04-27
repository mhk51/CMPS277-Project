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

from models.communityHub import CommunityHub
from models.publisher import Publisher
from models.genre import Genre
from models.server import Server
from models.user import User
from models.game import Game
from models.trophy import Trophy




@app.route('/home',methods = ['GET'])
def hello_word():
    return 'hello world'