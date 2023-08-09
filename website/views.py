from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import User, Club 
from . import db 

views = Blueprint("views", __name__)  

# The list of all the clubs the user is in:
clubsJoined = []

@views.route("/", methods=["GET", "POST"])
def home():
     print(f"Current user: {current_user}")
     # Finds the club the user joined:
     clubName = request.args.get("nameOfClub")
     # Adds new club to the club list:
     clubsJoined.append(clubName)
     # Printed for debugging:
     print(clubsJoined)
     # Finds the club the user wants to leave:
     clubToLeave = request.args.get("clubLeft")
     # Makes sure the user is already in that club:
     if clubToLeave in clubsJoined:
         # If they are, that club gets removed from the club list:
         clubsJoined.remove(clubToLeave)
         # Printed for debugging:
         print(clubsJoined)
     if request.method == "POST":
        boxname = request.form.get("nameofclub")
        return render_template("layout.html", boxname=boxname, clubsJoined=clubsJoined, club_info=Club.query.all(), user=current_user) 
    
     return render_template("layout.html", clubsJoined=clubsJoined, club_info=Club.query.all(), user=current_user)

@views.route("/clubs")
def clubs():
    return render_template("clubs.html", clubsJoined=clubsJoined, club_info=Club.query.all(), user=current_user)

@views.route("/createaclub", methods=["GET", "POST"])
def createaclub():
    # Accepting the post request:
    if request.method == "POST":
        club_name = request.form.get("clubname")
        president_email = request.form.get("presidentemail")
        vicepresident_email1 = request.form.get("vicepresidentemail1")
        vicepresident_email2 = request.form.get("vicepresidentemail2")
        vicepresident_email3 = request.form.get("vicepresidentemail3")
        advisor_email = request.form.get("advisoremail")
        room_number = request.form.get("roomnumber")
        start_time = request.form.get("clubstarttime")
        description = request.form.get("clubdescription")
        # Verifying the post request:
        # name = Club.query.filter_by(club_name=club_name).first() 
        # email = User.query.filter_by(email=email).first()
        # vpemail1 = User.query.filter_by(vicepresident_email1=vicepresident_email1).first()
        # vpemail2 = User.query.filter_by(vicepresident_email2=vicepresident_email2).first()
        # vpemail3 = User.query.filter_by(vicepresident_email3=vicepresident_email3).first()
        # if name:
        flash("Club name already in use. Try a different one!", category="error") 
        # elif not email:
            # flash("Email not found, try a different one.", category="error")
        # elif not vpemail1:
        flash(f"Email {vicepresident_email1} not found, make sure their account has been created.", category="error")
        # elif not vpemail2:
        flash(f"Email {vicepresident_email2} not found, make sure their account has been created.", category="error")
        # elif not vpemail3:
        flash(f"Email {vicepresident_email3} not found, make sure their account has been created.", category="error")
        # else: 
        new_club = Club(club_name=club_name, president_email=president_email, vicepresident_email1=vicepresident_email1, vicepresident_email2=vicepresident_email2, vicepresident_email3=vicepresident_email3, advisor_email=advisor_email, room_number=room_number, start_time=start_time, description=description)
        print(f"New Club Name: {new_club.club_name}, President: {new_club.president_email}, VP1: {new_club.vicepresident_email1}, VP2: {new_club.vicepresident_email2}, VP3: {new_club.vicepresident_email3}, Advisor: {new_club.advisor_email}, Room Number: {new_club.room_number}, Start Time: {new_club.start_time}, Description: {new_club.description}")
        db.session.add(new_club)
        db.session.commit()
        flash("Your new club has been created!", category="success")
        return render_template("layout.html", user=current_user)


    return render_template("createaclub.html", user=current_user)
