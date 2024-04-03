from . import db
from flask_login import UserMixin

# Flask Migration source - https://www.youtube.com/watch?v=dCym9EICKGQ
# flask db migrate
# flask db stamp head

# Better source - https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date
# flask db stamp head
# flask db migrate
# flask db upgrade

# Table representing the many to many relationship between User and Club. This table is made up of two columns for each foreign key of both users and clubs. 
joined_clubs = db.Table("joined_clubs",
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
    # Everytime a club is joined, add into this "clubs" column the id for that club (A list). - This is an easy and the best way to store and keep track of who is in which club and how many clubs a user is in. secondary links the User class to the club_joined table, which was created and initialized above. backref is how the users are stored in the Club model; they are stored as "members": 
    clubs = db.relationship("Club", secondary=joined_clubs, backref="members")
    is_leader = db.Column(db.Boolean)
    role = db.Column(db.String)

    def __str__(self):
        return self.email

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
    secret_password = db.Column(db.Integer)
    club_day = db.Column(db.String)
    status = db.Column(db.String)
    rehaan = db.Column(db.String)
    # Foreign Key - This column references a user's id in the User database class. - A one to many relationship:
    # user_id = db.Column(db.Integer, db.ForeignKey("user.id")) 
    # user = db.relationship("User", secondary="user_club", back_populates="club")

    def __str__(self):
        return self.club_name

# Setting up the Many-To-Many relationship between Clubs and Users (The association table): 
class UserClubs(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey(Club.id), primary_key=True)

class Info(db.Model):
    text_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    body = db.Column(db.String)
    subheader = db.Column(db.String)

    def __str__(self):
        return self.title
    
class Mentor(db.Model):
    mentor_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    # race = db.Column(db.String)
    # religion = db.Column(db.String)
    # gender = db.Column(db.String)
    # languages = db.Column(db.String)
    # academics = db.Column(db.String)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    path = db.Column(db.String)