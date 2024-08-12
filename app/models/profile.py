from app import db

class Profile(db.Model):
    __tablename__ = "profiles"
    
    id = db.Column(db.Integer, primary_key = True)
    #ForeignKey to User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #ForeignKey to Role
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    #Back references to User and Role
    user = db.relationship("User", back_populates = "profile")
    role = db.relationship("Role", back_populates = "profile")