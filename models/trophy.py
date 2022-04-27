from app import db 

class Trophy(db.Model):
    name = db.Column(db.String(30),primary_key = True)
    rarity = db.Column(db.String(30))
    points = db.Column(db.Integer)
    game_ID = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    user_name = db.Column(db.String(30),db.ForeignKey('user.user_name'),nullable = False)


    def __init__(self,name,rarity,points,game_ID,user_name):
        super(Trophy,self).__init__(name=name,rarity=rarity,point=points,game_ID=game_ID,user_name=user_name)
