from . import db
from flask_login import UserMixin

# Setting up the Many-To-Many relationship between Clubs and Users: 
clubs_joined = db.Table("clubs_joined",
                        db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                        db.Column("club_id", db.Integer, db.ForeignKey("club.id"))
                        )

class User(db.Model, UserMixin): 
    # Defining a schema, or a layout for some object to be stored in the database:
    # This (id) is the primary key, or the unique identifier for every User object created. This unique identifier value is stored as an Integer:
    id = db.Column(db.Integer, primary_key=True) 
    # Creates a new column for user emails and passwords. This will be stored as a String, with the max character limit of 150. Every user must have their own email, meaning the same email cannot be used twice across multiple accounts (will result in an error):
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150)) 
    # Everytime a club is joined, add into this "clubs" column the id for that club (A list). - This is an easy and the best way to store and keep track of who is in which club and how many clubs a user is in. backref is how the users are stored in the Club model; they are stored as "members": 
    clubs = db.relationship("Club", secondary=clubs_joined, backref="members") 

class Club(db.Model): 
    # Primary Key id:
    id = db.Column(db.Integer, primary_key=True) 
    club_name = db.Column(db.String(100), unique=True)
    president_email = db.Column(db.String(100))
    vicepresident_email1 = db.Column(db.String(100))
    vicepresident_email2 = db.Column(db.String(100))
    vicepresident_email3 = db.Column(db.String(100))
    advisor_email = db.Column(db.String(100))
    room_number = db.Column(db.Integer)
    start_time = db.Column(db.String(100))
    description = db.Column(db.String(5000))
    # Foreign Key - This column references a user's id in the User database class. - A one to many relationship:
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id")) 