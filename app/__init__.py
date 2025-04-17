from flask import Flask
from .models import db  # ← this imports your db instance
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()       # creates tables if not present
        register_routes(app)

    return app