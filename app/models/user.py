from app import db

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), index = True, unique = True, nullable = False)
    password_hash = db.Column(db.String(128))
    
    #ForeignKey to UserData
    userdata_id = db.Column(db.Integer, db.ForeignKey("userdata.id"))
    #Back references to userdata
    userdata = db.relationship("UserData", back_populates = "user")
    #One to One relationship with Profile
    profile = db.relationship("Profile", uselist = False, back_populates = "user")
    #One to Many relationship with CourseUser
    course_user = db.relationship("CourseUser", back_populates = "user")