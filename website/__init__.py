from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager 
# If doesn't work - pip install werkzeug==2.3.0
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail, Message
import os
from flask_migrate import Migrate
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select
from sqlalchemy import create_engine

# Initializing the SQL database:
db = SQLAlchemy()
DB_NAME = "database.db"

# Initializing the admin page:
admin = Admin()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "rehaan"
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://jlfpuxzdqrkneh:f3ca613563b5efcad1f6c485e7a27118b7cd0d78c2326a70ee98fb21d9f4c248@ec2-52-0-79-72.compute-1.amazonaws.com:5432/ddmnvas8sg8evg"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}" 
    migrate = Migrate(app, db)
    db.init_app(app) 
    # Configuring the mail messaging system:
    app.config["MAIL_SERVER"] = "smtp@googlemail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = "rehaan1099@gmail.com"
    app.config["MAIL_PASSWORD"] = "exeawwlbuwodiuso"
    app.config["MAIL_USE_TLS"] = True
    mail = Mail(app) 

    # Import the blueprints:
    from .views import views
    from .auth import auth
    from .clubs import clubs
    from .findamentor import findamentor

    # Import the User and Club classes
    from .models import User, Club, Info, Mentor

    with app.app_context():
        db.create_all()
        admin.init_app(app)

    # Adding both classes (User and Club) to the admin page:
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Club, db.session))
    admin.add_view(ModelView(Info, db.session))
    admin.add_view(ModelView(Mentor, db.session))

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
    app.register_blueprint(clubs, url_prefix="/")
    app.register_blueprint(findamentor, url_prefix="/")

    # Source: https://docs.sqlalchemy.org/en/20/core/pooling.html#pool-disconnects
    some_engine = create_engine(f"sqlite:///{DB_NAME}")

    @event.listens_for(some_engine, "engine_connect")
    def ping_connection(connection, branch):
        if branch:
            # this parameter is always False as of SQLAlchemy 2.0,
            # but is still accepted by the event hook.  In 1.x versions
            # of SQLAlchemy, "branched" connections should be skipped.
            return

        try:
            # run a SELECT 1.   use a core select() so that
            # the SELECT of a scalar value without a table is
            # appropriately formatted for the backend
            connection.scalar(select(1))
        except exc.DBAPIError as err:
            # catch SQLAlchemy's DBAPIError, which is a wrapper
            # for the DBAPI's exception.  It includes a .connection_invalidated
            # attribute which specifies if this connection is a "disconnect"
            # condition, which is based on inspection of the original exception
            # by the dialect in use.
            if err.connection_invalidated:
                # run the same SELECT again - the connection will re-validate
                # itself and establish a new connection.  The disconnect detection
                # here also causes the whole connection pool to be invalidated
                # so that all stale connections are discarded.
                connection.scalar(select(1))
            else:
                raise

    return app
