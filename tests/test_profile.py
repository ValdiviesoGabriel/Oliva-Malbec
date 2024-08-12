import unittest
import os
from app import db, create_app
from app.models.profile import Profile
from app.models.user import User
from app.models.role import Role

class TestProfileModel(unittest.TestCase):
    
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
        
    def test_profile_creation(self):
        user = User(email = "test@test.com")
        role = Role(name = "TEST")
        db.session.add(user)
        db.session.add(role)
        db.session.commit()
        
        profile = Profile(user_id = user.id, role_id = role.id)
        db.session.add(profile)
        db.session.commit()
        
        self.assertEqual(profile.user_id, 1)
        self.assertEqual(profile.role_id, 1)

if __name__ == "__main__":
    unittest.main()