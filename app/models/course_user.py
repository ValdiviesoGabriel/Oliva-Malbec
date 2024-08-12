from app import db

class CourseUser(db.Model):
    __tablename__ = "course-user"
    
    id = db.Column(db.Integer, primary_key = True)
    grade = db.Column(db.String(4), nullable = True)
    
    #ForeignKey to Course
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable = False)
    #ForeignKey to User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    #Many to One relationship with User
    user = db.relationship("User", back_populates = "course_user")
    #Many to One relationship with Course
    course = db.relationship("Course", back_populates = "course_user")