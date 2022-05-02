import email
from msilib.schema import Error
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




@app.route('/Homepage',methods =["GET"])
def home_page():
    return render_template('page2.html')


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



@app.route('/insertgame',methods = ['GET'])
def render_insert_game():
    genres = Genre.query.all()
    servers = Server.query.all()
    return render_template('InsertGame.html',genres=genres,servers=servers)

@app.route('/insertgame',methods = ['POST'])
def insert_game():
    name = request.form['name']
    genre = request.form['genre']
    rating = request.form['rating']
    game_instance = Game(name,genre,rating)
    genre_instance = Genre.query.filter_by(name = genre).first()
    if(genre_instance == None):
        genre_instance = Genre(genre)
        db.session.add(genre_instance)
        db.session.commit()
    db.session.add(game_instance)
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/insertplayer',methods = ['GET'])
def render_insert_player():
    return render_template('InsertPlayer.html')

@app.route('/insertplayer',methods =['POST'])
def insert_player():
    name = request.form['name']
    genre = request.form['genre']
    rating = request.form['rating']
    game_instance = Game(name,genre,rating)
    genre_instance = Genre.query.filter_by(name = genre).first()
    if(genre_instance == None):
        genre_instance = Genre(genre)
        db.session.add(genre_instance)
        db.session.commit()
    db.session.add(game_instance)
    db.session.commit()
    return redirect(url_for('home_page'))


@app.route('/insertpublisher',methods = ['GET'])
def render_insert_publisher():
    return render_template('InsertPublisher.html')

@app.route('/insertpublisher',methods = ['POST'])
def insert_publisher():
    name = request.form['name']
    location = request.form['location']
    rating = request.form['rating']
    est_year = request.form['est_year']
    publisher_instance = Publisher(name,rating,location,est_year)
    db.session.add(publisher_instance)
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/insertserver',methods = ['GET'])
def render_insert_server():
    return render_template('InsertServer.html')

@app.route('/insertserver',methods = ['POST'])
def insert_server():
    name = request.form['name']
    region = request.form['region']
    capacity = request.form['capacity']
    server_instance = Server(name,region,capacity)
    db.session.add(server_instance)
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/insertgenre',methods = ["GET"])
def render_insert_genre():
    return render_template('InsertGenre')

@app.route('/insertgenre',methods = ['POST'])
def insert_genre():
    name = request.form['name']
    genre_instance = Genre(name)
    db.session.add(genre_instance)
    db.session.commit()
    return redirect(url_for('render_insert_game'))