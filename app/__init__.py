from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#create DB object globally
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRATE_KEY'] = 'scerate-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.auth import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app
