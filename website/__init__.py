from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager 
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView

# Initializing the SQL database:
db = SQLAlchemy()
DB_NAME = "database.db"

# Initializing the admin page:
admin = Admin()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "rehaan"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}" 
    db.init_app(app) 

    # Import the blueprints:
    from .views import views 
    from .auth import auth

    # Import the User and Club classes
    from .models import User, Club 

    with app.app_context():
        db.create_all()
        admin.init_app(app)

    # Adding both classes (User and Club) to the admin page:
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Club, db.session))

    login_manager = LoginManager()
    # Where the user goes if they're not logged in. 
    login_manager.login_view = "auth.login" 
    # Tells the login manager which app is currently being used. 
    login_manager.init_app(app) 

    @login_manager.user_loader 
    def load_user(id): 
        # Tells flask how to load the user. By default, it looks for the primary key (id). 
        return User.query.get(int(id)) 

    # Register the blueprints with the Flask application:
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    return app
