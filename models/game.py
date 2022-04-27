from app import db 

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    rating = db.Column(db.String(30))
    no_of_purchases = db.Column(db.Integer)
    # Genre_Name
    # Server_Name
    # Server_Region

    def __init__(self, name, rating,no_of_purchases):
        super(Game, self).__init__(name = name,rating = rating,no_of_purchases = no_of_purchases)