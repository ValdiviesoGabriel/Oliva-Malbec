from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from app.config import factory
import os

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    app_context = os.getenv("FLASK_CONTEXT")

    app = Flask(__name__)
    config_object = factory(app_context if app_context else "development")
    app.config.from_object(config_object)

    ma.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.resources.home import home_bp
    app.register_blueprint(home_bp, url_prefix="/home")

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app