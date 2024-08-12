from app import db

class Role(db.Model):
    __tablename__ = "roles"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(32), unique = True)

    #One to One relationship with Profile
    profile = db.relationship("Profile", uselist = False, back_populates = "role")