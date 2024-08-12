from app import db

class UserData(db.Model):
    __tablename__ = "userdata"
    
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(32), nullable = True)
    last_name = db.Column(db.String(32), nullable = True)
    dni = db.Column(db.String(16), nullable = True, unique = True)
    phone = db.Column(db.String(32), nullable = True)
    address = db.Column(db.String(64), nullable = True)
    
    #One to One relationship with User
    user = db.relationship("User", uselist = False, back_populates = "userdata")