from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Club 
from . import db
import random
import smtplib
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

views = Blueprint("views", __name__)  

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    # Join / Leave Club Buttions functionality: 
    print(f"Current user: {current_user}")
    users = User.query.all()
    for user in users:
        if user.is_leader:
            print(user)
    join_club = request.args.get("joinClub")
    if join_club is not None:
        if Club.query.filter_by(club_name=join_club).first() in current_user.clubs:
            flash("You're already in that club.")
            print(f"{current_user} is already in {join_club}")
        else:
            print(f"User wants to join {join_club}")
            if Club.query.filter_by(club_name=join_club).first():
                print(f"{join_club} found!")
            else:
                print(f"{join_club} not found!")
            print(f"{Club.query.filter_by(club_name=join_club).first()}")
            current_user.clubs.append(Club.query.filter_by(club_name=join_club).first())
            print(current_user.clubs)
            db.session.commit()
            clubs = Club.query.all()
            for club in clubs:
                print(club.club_name) 
                print(club.members)
                print("---")
            users = User.query.all()
            for user in users:
                print(user.email)
                print(user.clubs)
                print("---")
            flash(f"{join_club} joined!", category="success")
    else:
        print(f"Request to join {join_club} failed!") 
    
    # Leave the club:
    leave_club = request.args.get("leaveClub")
    if leave_club is not None:
        print(current_user.clubs)
        leave_club_id = Club.query.filter_by(club_name=leave_club).first()
        print(leave_club_id)
        if leave_club_id in current_user.clubs:
            print(f"User wants to leave {leave_club}") 
            print(Club.query.filter_by(club_name=leave_club).first())
            current_user.clubs.remove(Club.query.filter_by(club_name=leave_club).first())
            db.session.commit()
            print(f"Successfully left {leave_club}")
            flash(f"Left {join_club}!", category="success")
            # return render_template("layout.html", club_info=Club.query.all(), user=current_user)
            print(f"Current user clubs: {current_user.clubs}")
        else:
            flash(f"You aren't in {join_club}!", category="error")
            # return render_template("layout.html", club_info=Club.query.all(), user=current_user)
            print(f"User is not in {leave_club}")

    # Club Password Verification:
    if request.method == "POST":
        club_password = request.form.get("connecttoclubnumber")
        clubs = Club.query.all()
        for club in clubs:
            print(club.secret_password)
        print(club_password)
        if Club.query.filter_by(secret_password=club_password).first():
            club_found = Club.query.filter_by(secret_password=club_password).first()
            print(club_found)
            flash("Club successfully found!", "success")
            print(club_found.members)
            current_user.is_leader = True
            return render_template("clubdashboard.html", club_info=Club.query.all(), user_info=User.query.all(), user=current_user)
        else:
            flash("No club found with matching code!", "error")
            print("None found")

    # Filter By Buttons Functionality:
    filterby = request.args.get("filterby")
    print(f"Filterby: {filterby}")
    '''
        Filter by list: 
            - clubsjoined
            - clubsnotjoined
            - morningclubs
            - afternoon clubs
    '''
    club_info=Club.query.all()
    if filterby == "clubsjoined":
        print("Clubs Joined!")
        print(current_user.clubs)
        # print(f"Club Info: {club_info}") 
        # return render_template("clubs.html", club_info=current_user.clubs, user=current_user)
        # return url_for("views.clubs")
    elif filterby == "clubsnotjoined":
        print("Clubs Not Joined!")
    elif filterby == "morningclubs":
        print("Morning Clubs!")
    elif filterby == "afternoonclubs":
        print("Afternoon Clubs!")

    return render_template("layout.html", club_info=Club.query.all(), joined_clubs=current_user.clubs, user=current_user)

@views.route("/clubs", methods=["GET", "POST"])
@login_required
def clubs():
    return render_template("clubs.html", club_info=current_user.clubs, user=current_user)

@views.route("/clubdashboard")
@login_required
def club_dashboard():
    # Remove a member:
    if request.method == "GET":
        remove_club = request.args.get("removeClub")
        remove_member = request.args.get("removeMember")
        print(f"Remove Member: {remove_member}")
        print(f"Remove Club: {remove_club}")
        print(f"Remove Member: {User.query.filter_by(id=remove_member).first()}")
        member = User.query.filter_by(id=remove_member).first()
        print(f"Remove Club: {Club.query.filter_by(id=remove_club).first()}")
        club = Club.query.filter_by(id=remove_club).first()
        print(current_user)
        print(current_user.clubs)
        print(f"Member: {member}")
        all_clubs = Club.query.all()
        for club in all_clubs:
            for club_member in club.members:
                # print(club_member.clubs)
                print(club_member)
                if member == club_member:
                    print(f"Member Found: {club_member}")
                    if Club.query.filter_by(id=remove_club).first() in member.clubs:
                        member.clubs.remove(Club.query.filter_by(id=remove_club).first())
                    else:
                        print(f"{member} is not in {remove_club}")
                    continue
                else:
                    print("Member not found")
        # print(member.clubs)
        # member.clubs.remove(Club.query.filter_by(id=remove_club).first())

    return render_template("clubdashboard.html", club_info=Club.query.all(), user_info=User.query.all(), user=current_user)

@views.route("/createaclub", methods=["GET", "POST"])
@login_required
def createaclub():
    days_selected = request.args.get("clubDays")
    print(f"Days selected: {days_selected}")
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
        president = User.query.filter_by(email=president_email).first()
        president.is_leader = True 
        if vicepresident_email1:
            vp1 = User.query.filter_by(email=vicepresident_email1).first()
            vp1.is_leader = True
        if vicepresident_email2:
            vp2 = User.query.filter_by(email=vicepresident_email2).first()
            vp2.is_leader = True
        if vicepresident_email3:
            vp3 = User.query.filter_by(email=vicepresident_email3).first()
            vp3.is_leader = True
        pres = User.query.filter_by(email=president_email).first()
        pres.role = "Leader"
        print(f"President: {president}")
        # Make sure the club president is the person who is currently logged in:
        if president_email == current_user.email:
            print("True")
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
        # Making the random password:
        secret_password = random.randint(100, 1000000)
        print(f"Secret password: {secret_password}")
        new_club = Club(club_name=club_name, president_email=president_email, vicepresident_email1=vicepresident_email1, vicepresident_email2=vicepresident_email2, vicepresident_email3=vicepresident_email3, advisor_email=advisor_email, room_number=room_number, start_time=start_time, description=description, secret_password=secret_password)
        print(f"New Club Name: {new_club.club_name}, President: {new_club.president_email}, VP1: {new_club.vicepresident_email1}, VP2: {new_club.vicepresident_email2}, VP3: {new_club.vicepresident_email3}, Advisor: {new_club.advisor_email}, Room Number: {new_club.room_number}, Start Time: {new_club.start_time}, Description: {new_club.description}")
        db.session.add(new_club)
        db.session.commit()
        pres.clubs.append(Club.query.filter_by(club_name=club_name).first())
        if vicepresident_email1:
            vp1.clubs.append(Club.query.filter_by(club_name=club_name).first())
        if vicepresident_email2:
            vp2.clubs.append(Club.query.filter_by(club_name=club_name).first())
        if vicepresident_email3:
            vp3.clubs.append(Club.query.filter_by(club_name=club_name).first())
        flash("Your new club has been created!", category="success")
        return render_template("layout.html", user=current_user, club_info=Club.query.all())

    return render_template("createaclub.html", user=current_user)

# @views.route("/send_email/<email>")
# def send_email(email):
#         # Sending the email:
#         email_title = "Your club has been successfully added!"
#         sender = "crlsclubfinder@clubfinder.com"
#         message = Message(email_title, sender=sender, recipients=[current_user.email])
#         email_body = "Your secret club password is 1"
#         message.body = ""
#         data = {
#             "app_name": "clubfinder",
#             "title": email_title,
#             "body": email_body,
#         }
#         message.html = render_template("email.html", data=data)
#         try: 
#             Mail.send(message)
#             return "Email sent"
#         except Exception as e:
#             print(e)
#             return "The email was not sent"

# @views.route("/email")
# def email():
#     # Sending the email:
#     email_title = "Your club has been successfully added!"
#     sender = "crlsclubfinder@clubfinder.com"
#     msg = Message(email_title, sender=sender, recipients=[current_user.email])
#     email_body = "Your secret club password is 1"
#     msg.body = ""
#     data = {
#         "app_name": "clubfinder",
#         "title": email_title,
#         "body": email_body,
#     }
#     msg.html = render_template("email.html", data=data)
#     try: 
#         Mail.send(msg, sender)
#         return "Email sent"
#     except Exception as e:
#         print(e)
#         return f"The email was not sent. Error: {e}"
        
#     return render_template("email.html")

@views.route("/send_email", methods=["GET", "POST"])
def send_email():
    email_address = "rehaan1099@gmail.com" # request.form['address']
    email_subject = "Test Email!" # request.form['subject']
    email_message = "This email works ok!" # request.form['message']

    sender_email = 'youremail'
    sender_password = 'your password'
    receiver_email = email_address

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = email_subject
    message.attach(MIMEText(email_message, 'plain'))

    # try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

    #     return 'Email Sent!'
    # except Exception as e:
    #     return str(e)

# Search:
@views.route("/search")
def search():
    # q gets the value of q, which was passed in from the input field from the HTML. 
    q = request.args.get("q")
    print(q)

    if q:
        # If the user types something in, all of teh clubs will filter if they have (or contain) the value of q. 
        results = Club.query.filter(Club.club_name.contains(q) | Club.president_email.contains(q)).order_by(Club.club_name.asc()).all()
    else:
        # Else, if there is no value in q, results will be set to every item in the Club class. 
        results = Club.query.all()
    
    return render_template("searchresults.html", results=results)

@views.route("/joinleavebuttons")
def joinleavebuttons():
    return render_template("joinleavebuttons.html", club_info=Club.query.all(), joined_clubs=current_user.clubs, user=current_user)