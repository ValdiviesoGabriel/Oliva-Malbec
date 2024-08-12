import unittest
import os
from app import db, create_app
from app.models.course import Course
from app.services.fetchers import *

class TestCourseModel(unittest.TestCase):
    
    def setUp(self):
        os.environ["FLASK_CONTEXT"] = "testing"
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
    def tearDown(self):
        db.session.rollback()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_course_creation(self):
        course = Course(name = "test")
        db.session.add(course)
        db.session.commit()
        
        fetched_course = fetch_course(course.id)
        self.assertIsNotNone(fetched_course)
        self.assertEqual(fetched_course.name, "test")

if __name__ == "__main__":
    unittest.main()