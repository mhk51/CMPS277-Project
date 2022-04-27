from app import db 

class Publisher(db.Model):
    name = db.Column(db.String(30),primary_key = True)
    rating = db.Column(db.String(30))
    location = db.Column(db.String(30))
    year_of_Est = db.Column(db.DateTime) 

    def __init__(self,name,rating,location,year_of_Est):
        super(Publisher,self).__init__(name=name,rating = rating,location = location,year_of_Est = year_of_Est)