import unittest
import os
from flask import Flask
from flask_jwt_extended import create_access_token
from app import db, create_app
from app.models.user import User
from app.models.profile import Profile
from app.models.role import Role
from app.models.user_data import UserData
from app.services.fetchers import *
from app.utils.initializers import initialize_roles
from app.utils.security import check_password, set_password

class TestUserBP(unittest.TestCase):
    
    def setUp(self):
        os.environ["FLASK_CONTEXT"] = "testing"
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        initialize_roles()
        
        #ADMIN USER
        self.user = User(email = "admin@test.com", userdata = UserData())
        self.user.password_hash = set_password("admin")
        role = Role.query.filter_by(name = "ADMINISTRADOR").first()
        self.profile = Profile(user_id = self.user.id, role_id = role.id)
        
        db.session.add(self.user)
        db.session.add(self.profile)
        db.session.commit()
        
        self.token = create_access_token(identity = {"id": self.user.id, "role" : role.name})
        
        
    def tearDown(self):
        db.session.rollback()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        data = {
            "email" : "test@test.com",
            "password" : "test",
            "role" : "ADMINISTRADOR"
        }
        
        response = self.client.post("/users", json = data, headers = {"Authorization": f"Bearer {self.token}"})
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["message"], "User registered successfully")
        
        created_user_id = response.json["id"]
        created_user = fetch_user(created_user_id)
        role = Role.query.filter_by(name = "ADMINISTRADOR").first()
        created_profile = Profile.query.filter_by(user_id = created_user_id).first()
        
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.email, "test@test.com")
        self.assertTrue(check_password(hash = created_user.password_hash, password = "test"))
        
        self.assertIsNotNone(created_profile)
        self.assertEqual(created_profile.role_id, role.id)
        self.assertEqual(created_profile.user_id, created_user_id)
    
    def test_get_all_users(self):
        user1 = User(email = "test1@test.com", userdata = UserData())
        user2 = User(email = "test2@test.com", userdata = UserData())
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        response = self.client.get("/users", headers = {"Authorization": f"Bearer {self.token}"})
        
        self.assertEqual(response.status_code, 200)
        users = response.json["users"]
        
        self.assertIsNotNone(users)
        
        users_emails = [user["email"] for user in users]
        self.assertIn("test1@test.com", users_emails)
        self.assertIn("test2@test.com", users_emails)
        
    def test_get_user_by_id(self):
        user = User(email = "test@gmail.com", userdata = UserData())
        db.session.add(user)
        db.session.commit()
        
        user_id = user.id
        response = self.client.get(f"/users/{user_id}", headers = {"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["user"]["id"], user_id)
        self.assertEqual(response.json["user"]["email"], "test@gmail.com")
        
    def test_update_user(self):
        user = User(email = "test@gmail.com", userdata = UserData())
        db.session.add(user)
        db.session.commit()
        
        data = {
            "email" : "update@gmail.com",
            "first_name" : "test",
            "last_name" : "test"
        }
        user_id = user.id
        response = self.client.put(f"/users/{user_id}", json = data, headers = {"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "User updated successfully")
        
        user_updated = fetch_user(user_id)
        self.assertIsNotNone(user_updated)
        self.assertEqual(user_updated.email, "update@gmail.com")
        self.assertEqual(user_updated.userdata.first_name, "test")
        self.assertEqual(user_updated.userdata.last_name, "test")
    
    def test_delete_user(self):
        user = User(email = "test@test.com", userdata = UserData())
        db.session.add(user)
        db.session.commit()
        
        user_id = user.id
        response = self.client.delete(f"/users/{user_id}", headers = {"Authorization": f"Bearer {self.token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "User deleted successfully")
        
if __name__ == "__main__":
    unittest.main()