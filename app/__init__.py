from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from app.config import factory
import os

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    app_context = os.getenv("FLASK_CONTEXT")
    app = Flask(__name__)
    config_object = factory(app_context if app_context else "development")
    app.config.from_object(config_object)
    
    #Blueprints
    from app.resources.auth import auth_bp
    from app.resources.users import user_bp
    from app.resources.courses import course_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(course_bp)
    
    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    from app.models.user_data import UserData
    from app.models.user import User
    from app.models.role import Role
    from app.models.profile import Profile
    from app.models.course import Course
    from app.models.course_user import CourseUser
    
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}
    
    return app