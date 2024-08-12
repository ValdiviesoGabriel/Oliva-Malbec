from app import db

class Course(db.Model):
    __tablename__ = "courses"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False)
    
    #One to Many relationship with CourseUser
    course_user = db.relationship("CourseUser", back_populates = "course")