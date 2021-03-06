import email
from msilib.schema import Error
from operator import ge
import re
from turtle import pu
from flask import Flask, redirect, render_template, request, session, url_for
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

app.secret_key = "super secret key"

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
    session['token'] = user_name
    if user_instance is None:
        return render_sign_in()
    
    if not bcrypt.check_password_hash(user_instance.hashed_password, password):
        return render_sign_in()
    return render_template('page2.html')
        
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
    session['token'] = user_name
    return redirect(url_for('home_page'))



@app.route('/insertgame',methods = ['GET'])
def render_insert_game():
    genres = Genre.query.all()
    servers = Server.query.all()
    return render_template('InsertGame.html',genres=genres,servers=servers)

@app.route('/insertgame',methods = ['POST'])
def insert_game():
    name = request.form['name']
    genre = request.form.get('genres')
    rating = request.form['rating']
    server = request.form['servers'].split(",")
    server_name = server[0]
    server_region = server[1]
    game_instance = Game(name,genre,rating,server_name =server_name,server_region= server_region)
    db.session.add(game_instance)
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/insertcommunity',methods = ['GET'])
def render_insert_community():
    return render_template('InsertCommunity.html')

@app.route('/insertcommunity',methods =['POST'])
def insert_community():
    name = request.form['name']
    community_instance = Community(name)
    db.session.add(community_instance)
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/followcommunity',methods = ['GET'])
def render_follow_community():
    communities = Community.query.all()
    return render_template('followCommunity.html',communities=communities)

@app.route('/followcommunity',methods = ["POST"])
def follow_community():
    user_name = session['token']
    user_instance = User.query.get(user_name)
    community = request.form["communities"]
    community_instance = Community.query.get(community)
    print(community_instance)
    community_instance.users.append(user_instance)
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
    return render_template('InsertGenre.html')

@app.route('/insertgenre',methods = ['POST'])
def insert_genre():
    name = request.form['name']
    genre_instance = Genre(name)
    db.session.add(genre_instance)
    db.session.commit()
    return redirect(url_for('render_insert_game'))



@app.route('/playgame',methods = ['GET'])
def render_play_game():
    games = Game.query.all()
    return render_template('playGame.html',games = games)

@app.route('/playgame',methods = ['POST'])
def play_game():
    user_name = session['token']
    user_instance = User.query.filter_by(user_name=user_name).first()
    game = request.form['games'].split(",")
    game_id = game[0]
    game_instance = Game.query.get(game_id)
    game_instance.players.append(user_instance)
    db.session.commit()
    return redirect(url_for('home_page'))


@app.route('/followpublisher',methods = ['GET'])
def render_follow_publisher():
    publishers = Publisher.query.all()
    return render_template('followPublisher.html',publishers=publishers)

@app.route('/followpublisher',methods = ['POST'])
def follow_publisher():
    user_name = session['token']
    user_instance = User.query.get(user_name)
    publisher_name = request.form['publishers']
    publisher_instance = Publisher.query.get(publisher_name)
    publisher_instance.followers.append(user_instance)
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/connectserver',methods = ['GET'])
def render_connect_server():
    servers = Server.query.all()
    return render_template('connectServer.html',servers = servers)

@app.route('/connectserver',methods = ['POST'])
def connect_server():
    user_name = session['token']
    user_instance = User.query.get(user_name)
    server = request.form['servers'].split(',')
    server_name = server[0]
    server_region = server[1]
    server_instance = Server.query.get((server_name,server_region))
    server_instance.users.append(user_instance)
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/updategame',methods = ["GET"])
def render_update_game():
    genres = Genre.query.all()
    servers = Server.query.all()
    games = Game.query.all()
    return render_template('GameUpdate.html',servers=servers,genres=genres,games=games)

@app.route('/updategame',methods = ['POST'])
def update_game():
    game = request.form['games'].split(',')
    game_id = game[0]
    game_instance = Game.query.get(game_id)
    name = request.form['name']
    genre = request.form.get('genres')
    rating = request.form['rating']
    server = request.form['servers'].split(",")
    server_name = server[0]
    server_region = server[1]
    game_instance.name = name
    game_instance.genre_name = genre
    game_instance.rating = rating
    game_instance.server_Name = server_name
    game_instance.server_Region = server_region
    db.session.commit()
    return redirect(url_for('home_page'))


@app.route('/updatepublisher',methods = ["GET"])
def render_update_publisher():
    publishers = Publisher.query.all()
    return render_template('PublisherUpdate.html',publishers = publishers)

@app.route('/updatepublisher',methods = ["POST"])
def update_publisher():
    publisher = request.form['publishers']
    location = request.form['location']
    rating = request.form['rating']
    est_year = request.form['est_year']

    publisher_instance = Publisher.query.get(publisher)
    publisher_instance.location = location
    publisher_instance.rating = rating
    publisher_instance.year_of_Est = est_year
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/mygames',methods = ['GET'])
def render_my_games():
    user_name = session['token']
    games = Game.query.join(User,Game.players).filter_by(user_name=user_name)
    return render_template('myGames.html',games=games)


@app.route('/mypublishers',methods = ['GET'])
def render_my_publishers():
    user_name = session['token']
    publishers = Publisher.query.join(User,Publisher.followers).filter_by(user_name=user_name)
    return render_template('myPublishers.html',publishers=publishers)

@app.route('/mycommunities',methods = ['GET'])
def render_my_communities():
    user_name = session['token']
    communities = Community.query.join(User,Community.users).filter_by(user_name=user_name)

    return render_template('myCommunities.html',communities=communities)




@app.route('/retreivegames',methods = ["GET"])
def render_retrieve_games():
    games = Game.query.all()
    return render_template('retrievegames.html',games=games)

@app.route('/retreivegames',methods = ['POST'])
def delete_game():
    game_name = request.form['game']
    game_instance = Game.query.filter_by(name= game_name).first()
    db.session.delete(game_instance)
    db.session.commit()
    return redirect(url_for('home_page'))


@app.route('/retreivecommunities',methods = ["GET"])
def render_retrieve_communities():
    communities = Community.query.all()
    return render_template('retrievecommunities.html',communities=communities)


@app.route('/retreivecommunities',methods = ['POST'])
def delete_community():
    name = request.form['community']
    community_instance = Community.query.get(name)
    db.session.delete(community_instance)
    db.session.commit()
    return redirect(url_for('home_page'))


@app.route('/retreivepublishers',methods = ["GET"])
def render_retrieve_publishers():
    publishers = Publisher.query.all()
    return render_template('retrievepublishers.html',publishers=publishers)

@app.route('/retreivepublishers',methods = ['POST'])
def delete_publisher():
    name = request.form['publisher']
    publisher_instance = Publisher.query.get(name)
    db.session.delete(publisher_instance)
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/retreiveservers',methods = ["GET"])
def render_retrieve_servers():
    servers = Server.query.all()
    return render_template('retrieveservers.html',servers=servers)


