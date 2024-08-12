import unittest
import os
from flask import Flask
from app import db, create_app
from app.models.profile import Profile
from app.models.user import User
from app.utils.initializers import initialize_roles
from app.utils.security import set_password

class TestAuthBP(unittest.TestCase):
    
    def setUp(self):
        os.environ["FLASK_CONTEXT"] = "testing"
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        initialize_roles()
        
    def tearDown(self):
        db.session.rollback()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_login(self):
        user = User(email = "test@test.com")
        user.password_hash = set_password("test")
        db.session.add(user)
        db.session.commit()
        
        profile = Profile(user_id = user.id, role_id = 1)
        db.session.add(profile)
        db.session.commit()
        
        data = {
            "email": "test@test.com",
            "password": "test"
        }
        
        data2 = {
            "email": "test@test.com",
            "password" : "123"
        }
        
        response = self.client.post("/login", json = data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json)
        
        response2 = self.client.post("/login", json = data2)
        self.assertEqual(response2.status_code, 401)