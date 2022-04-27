from app import db

class CommunityHub(db.Model):
    name = db.Column(db.String(30),primary_key = True)

    def __init__(self,name):
        super(CommunityHub,self).__init__(name = name)