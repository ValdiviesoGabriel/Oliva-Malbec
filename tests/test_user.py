import unittest
import os
from app import db, create_app
from app.models.user import User
from app.services.fetchers import *
from app.utils.security import set_password, check_password

class TestUserModel(unittest.TestCase):
    
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
        
    def test_user_creation(self):
        user = User(email = "test@test.com")
        user.password_hash = set_password("test")
        db.session.add(user)
        db.session.commit()
        
        fetched_user = fetch_user(user.id)
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.email, "test@test.com")
        self.assertTrue(check_password(hash = fetched_user.password_hash, password = "test"))
        
if __name__ == "__main__":
    unittest.main()