from app import db,bcrypt,datetime


releases = db.Table('releases',
    db.Column('publisher_name', db.String(30), db.ForeignKey('publisher.name'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)
updates = db.Table('updates',
    db.Column('publisher_name', db.String(30), db.ForeignKey('publisher.name'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

following = db.Table('following',
    db.Column('publisher_name', db.String(30), db.ForeignKey('publisher.name'), primary_key=True),
    db.Column('user_name', db.String(30), db.ForeignKey('user.user_name'), primary_key=True)
)

playing = db.Table('playing',
    db.Column('user_name', db.String(30), db.ForeignKey('user.user_name'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)


class Community(db.Model):
    name = db.Column(db.String(30),primary_key = True)
    users = db.relationship('User', backref='community', lazy=True)

    def __init__(self,name):
        super(Community,self).__init__(name = name)

class Genre(db.Model):
    name = db.Column(db.String(30),primary_key = True)
    games = db.relationship('Game', backref='genre', lazy=True)

    def __init__(self,name):
        super(Genre,self).__init__(name = name)

class Server(db.Model):
    name = db.Column(db.String(30),primary_key = True)
    region = db.Column(db.String(30),primary_key = True)
    capacity = db.Column(db.Integer)
    users = db.relationship('User',backref = 'server',lazy = True)
    games = db.relationship('Game',backref = 'server',lazy = True)

    def __init__(self,name,region,capacity):
        super(Server,self).__init__(name = name,region = region,capacity = capacity)

class Publisher(db.Model):
    name = db.Column(db.String(30),primary_key = True)
    rating = db.Column(db.String(30))
    location = db.Column(db.String(30))
    year_of_Est = db.Column(db.DateTime)
    followers = db.relationship('User', secondary=following, backref='followers')
    games_released = db.relationship('Game', secondary=releases, backref='released')
    games_updated = db.relationship('Game', secondary=updates, backref='updated')

    def __init__(self,name,rating,location,year_of_Est):
        super(Publisher,self).__init__(name=name,rating = rating,location = location,year_of_Est = year_of_Est)


class User(db.Model):
    user_name = db.Column(db.String(30), primary_key=True,unique = True)
    hashed_password = db.Column(db.String(128))
    cart_balance = db.Column(db.Float)
    year_of_registration = db.Column(db.DateTime)
    nationality = db.Column(db.String(30),nullable=True)
    email = db.Column(db.String(30),unique = True,nullable=True)
    community_Name = db.Column(db.String(30), db.ForeignKey('community.name'), nullable=True)
    server_Name = db.Column(db.String(30),nullable = True)
    server_Region = db.Column(db.String(30),nullable = True)
    __table_args__ = (db.ForeignKeyConstraint([server_Name, server_Region],['server.name', 'server.region']),{})
    trophies = db.relationship('Trophy',backref = 'user',lazy = True)

    def __init__(self, user_name, password,email = None,nationality = None,community_Name = None,server_Name = None,server_Region = None):
        super(User, self).__init__(user_name=user_name,community_Name = community_Name,server_Name =server_Name,server_Region=server_Region)
        self.hashed_password = bcrypt.generate_password_hash(password)
        self.cart_balance = 0.0
        self.year_of_registration = datetime.datetime.now()
        self.nationality = nationality
        self.email = email


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    rating = db.Column(db.String(30))
    no_of_purchases = db.Column(db.Integer)
    genre_name = db.Column(db.String(30),db.ForeignKey('genre.name'),nullable = False)
    server_Name = db.Column(db.String(30),nullable = True)
    server_Region = db.Column(db.String(30),nullable = True)
    __table_args__ = (db.ForeignKeyConstraint([server_Name, server_Region],['server.name', 'server.region']),{})
    players = db.relationship('User', secondary=playing, backref='players')

    def __init__(self, name, rating,no_of_purchases):
        super(Game, self).__init__(name = name,rating = rating,no_of_purchases = no_of_purchases)


class Trophy(db.Model):
    name = db.Column(db.String(30),primary_key = True)
    rarity = db.Column(db.String(30))
    points = db.Column(db.Integer)
    game_ID = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    user_name = db.Column(db.String(30),db.ForeignKey('user.user_name'),nullable = False)


    def __init__(self,name,rarity,points,game_ID,user_name):
        super(Trophy,self).__init__(name=name,rarity=rarity,point=points,game_ID=game_ID,user_name=user_name)

