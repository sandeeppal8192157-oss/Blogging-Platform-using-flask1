from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my_secret_development_key' 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # This turns on the login system
    login_manager.init_app(app)
    login_manager.login_view = 'main.login' 

    from app.routes import main
    app.register_blueprint(main)
    
    return app