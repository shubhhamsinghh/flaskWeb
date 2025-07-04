from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager



#create DB object globally
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-development-secret-key'
    app.config['ENV'] = 'development' 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskAuth.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    from app.models import User

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(url_for('auth.login'))

    @app.context_processor
    def current_year():
        return {'current_year': datetime.now().year}

    return app

