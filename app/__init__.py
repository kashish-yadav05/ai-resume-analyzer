import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "magical"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ai_resume_analyzer.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.main import main_bp
    from app.routes.resume import resume_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        from app.models import User, Resume
        db.create_all()

    return app