from app import db

class Genre(db.Model):
    name = db.Column(db.String(30),primary_key = True)

    def __init__(self,name):
        super(Genre,self).__init__(name = name)