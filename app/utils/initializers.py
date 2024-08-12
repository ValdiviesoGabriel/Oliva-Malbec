from app import db
from app.models.profile import Profile
from app.models.role import Role
from app.models.user import User
from app.models.user_data import UserData
from app.utils.security import set_password

def initialize_roles():
    role_names = ["ESTUDIANTE", "DOCENTE", "ADMINISTRADOR"]
    for role_name in role_names:
        if not Role.query.filter_by(name=role_name).first():
            role = Role(name=role_name)
            db.session.add(role)
        db.session.commit()

def initialize_admin():
    if not User.query.filter_by(email = "admin@admin.com").first():
        userdata = UserData()
        db.session.add(userdata)
        db.session.commit()
        
        admin = User(email = "admin@admin.com", userdata = userdata)
        admin.password_hash = (set_password("admin"))
        db.session.add(admin)
        db.session.commit()
        
        role = Role.query.filter_by(name = "ADMINISTRADOR").first()
        profile = Profile(user_id = admin.id, role_id = role.id)
        db.session.add(profile)
        db.session.commit()