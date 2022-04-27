from calendar import c
from app import db

class Server(db.Model):
    name = db.Column(db.String(30),primary_key = True)
    region = db.Column(db.String(30),primary_key = True)
    capacity = db.Column(db.Integer)

    def __init__(self,name,region,capacity):
        super(Server,self).__init__(name = name,region = region,capacity = capacity)