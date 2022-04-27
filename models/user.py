from app import db,bcrypt,ma,datetime


class User(db.Model):
    user_name = db.Column(db.String(30), primary_key=True,unique = True)
    hashed_password = db.Column(db.String(128))
    cart_balance = db.Column(db.Float)
    year_of_registration = db.Column(db.DateTime)
    nationality = db.Column(db.String(30))
    email = db.Column(db.String(30),unique = True)
    # community_Name = db.Column(db.String(30),db.ForeignKey('CommunityHub.name'),nullable = True)
    server_Name = db.Column(db.String(30),db.ForeignKey('server.name'),nullable = True)
    server_Region = db.Column(db.String(30),db.ForeignKey('server.region'),nullable = True)

    def __init__(self, user_name, password,nationality,email,community_Name = None,server_Name = None,server_Region = None):
        super(User, self).__init__(user_name=user_name,community_Name = community_Name,server_Name =server_Name,server_Region=server_Region)
        self.hashed_password = bcrypt.generate_password_hash(password)
        self.cart_balance = 0.0
        self.year_of_registration = datetime.datetime.now()
        self.nationality = nationality
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_name")
        model = User
