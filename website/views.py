from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from .models import User, Club 
from .sendmail import send_mail
from . import db
import random
import smtplib
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_session import Session
import datetime 

views = Blueprint("views", __name__)  

# If the club password is correct / found:
def check_club_pass(num):
    if num == 1:
        return False
    if num == 2:
        return True
    
def email_failure(error_message, current_time, problem_description):
    email_sender = "crlsclubfinder@gmail.com"
    email_password = "wmzhhaxtzqnvyuze"
    email_receiver = "rehaan1099@gmail.com"
    subject = f"CLUBFINDER PROBLEM: {problem_description}"
    body = f"PROBLEM at {current_time}: {problem_description}: \n {error_message}"
    send_mail(email_sender=email_sender, email_password=email_password, email_receiver=email_receiver, subject=subject, body=body)
    return True

# Actually creates the new club and commits it to the database:
def create_new_club(club_name, president_email, vicepresident_email1, vicepresident_email2, vicepresident_email3, advisor_email, room_number, start_time, description, secret_password, club_day):
    if "club_confirmed" in session:
        if session["club_confirmed"] == "YES":
            new_club = Club(club_name=club_name, president_email=president_email, vicepresident_email1=vicepresident_email1, vicepresident_email2=vicepresident_email2, vicepresident_email3=vicepresident_email3, advisor_email=advisor_email, room_number=room_number, start_time=start_time, description=description, secret_password=secret_password, club_day=club_day)
            print(f"New Club Name: {new_club.club_name}, President: {new_club.president_email}, VP1: {new_club.vicepresident_email1}, VP2: {new_club.vicepresident_email2}, VP3: {new_club.vicepresident_email3}, Advisor: {new_club.advisor_email}, Room Number: {new_club.room_number}, Start Time: {new_club.start_time}, Description: {new_club.description}, Club Day(s): {new_club.club_day}")
            db.session.add(new_club)
            db.session.commit()
            return True
        return False
    return False

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    # if sessio
    if request.method == "POST":
        tester = request.form.get("email")
        if tester:
            return redirect("/clubdashboard/info")
            # return render_template("clubdashboard.html", club_info=Club.query.all(), user_info=User.query.all(), user=current_user)
    print("32")
    # if current_user is not None:
    #     cur_us = User.query.filter_by(email=current_user.email).first()
    #     print("34")
    #     if cur_us.email == "rehaan1099@gmail.com":
    #         print("36")
    #         cur_us.role = "Admin"
    #         db.session.commit()
    #         print(f"38 - done! {cur_us.role}")
    #     print(f"39 - {current_user.role}")
    # Join / Leave Club Buttions functionality: 
    print(f"Current user: {current_user}")
    users = User.query.all()
    for user in users:
        if user.is_leader:
            print(user)
            
    join_club = request.args.get("joinClub")
    if join_club is not None:
        if Club.query.filter_by(id=join_club).first() in current_user.clubs:
            flash("You're already in that club.")
            print(f"{current_user} is already in {join_club}")
            return redirect("/")
        else:
            print(f"User wants to join {join_club}")
            if Club.query.filter_by(id=join_club).first():
                print(f"{join_club} found!")
            else:
                print(f"{join_club} not found!")
            print(f"{Club.query.filter_by(id=join_club).first()}")
            joined_club = Club.query.filter_by(id=join_club).first()
            current_user.clubs.append(joined_club)
            print(current_user.clubs)
            flash(f"Successfully joined {joined_club}!", "success")
            db.session.commit()
            email_sender = "crlsclubfinder@gmail.com"
            email_password = "wmzhhaxtzqnvyuze" 
            email_receiver = current_user.email
            subject = f"Successfully joined {joined_club}!"
            body = f'''Hello! 
You have successfully joined {joined_club}!
Here is some more information on this club:

President: {joined_club.president_email}
Advisor: {joined_club.advisor_email}
Room Number: {joined_club.room_number}
Start Time: {joined_club.start_time}
Meets on {joined_club.club_day}
Club Description: {joined_club.description}

Do not respond to this email.

'''
            try:
                send_mail(email_sender=email_sender, email_password=email_password, email_receiver=email_receiver, subject=subject, body=body)
                return redirect("/")
            except Exception as e:
                print("Could not send email")
                current_time = datetime.datetime.now()
                problem_description = "Sending joined club confirmation email"
                email_failure(error_message=e, current_time=current_time, problem_description=problem_description)
                return redirect("/")
            # return redirect(url_for(".home"))
    else:
        print(f"Request to join {join_club} failed!") 
    
    # Leave the club:
    leave_club = request.args.get("leaveClub")
    if leave_club is not None:
        print(current_user.clubs)
        leave_club_id = Club.query.filter_by(id=leave_club).first()
        print(leave_club_id)
        if leave_club_id in current_user.clubs:
            print(f"User wants to leave {leave_club}") 
            print(Club.query.filter_by(id=leave_club).first())
            left_club = Club.query.filter_by(id=leave_club).first()
            current_user.clubs.remove(left_club)
            db.session.commit()
            print(f"Successfully left {left_club}")
            flash(f"Left {left_club}!", "success")
            print(f"Current user clubs: {current_user.clubs}")
            return redirect("/")
        else:
            flash(f"You aren't in {join_club}!", "error")
            print(f"User is not in {leave_club}")
            return redirect("/")

    # Club Password Verification:
    if request.method == "POST":
        club_password = request.form.get("connecttoclubnumber")
        is_a_club = Club.query.filter_by(secret_password=club_password).first()
        if current_user.role == "Advisor":
            if is_a_club:
                if is_a_club.status == "Pending":
                    is_a_club.status = "Approved"
                    db.session.commit()
                    flash(f"Successfully verified {is_a_club.club_name}", "success")
                    return redirect("/")
                elif is_a_club.status == "Approved":
                    flash(f"{is_a_club.club_name} already verified.", "error")
                    return redirect("/")
        else:
            flash("Only advisors can verify clubs!", "error")
            return redirect("/")
        clubs = Club.query.all()
        for club in clubs:
            print(club.secret_password)
        print(club_password)
    
        if "secret_password" in session:
            print(f"105 - {session['secret_password']}")
            print(f"106 - club password: {club_password}")
            club_password = int(club_password)
            print(session["secret_password"] == club_password)
            # print(club_password.isnumeric())
            if session['secret_password'] == club_password:
                print("108 - success")
        # if Club.query.filter_by(secret_password=club_password).first():
                # if current_user.role == "Advisor":
                # club_found = Club.query.filter_by(secret_password=club_password).first()
                # print(club_found)
                # flash("Club successfully found!", "success")
                # print(club_found.members)
                current_user.is_leader = True
                db.session.commit()
                session["club_confirmed"] = "YES"
                # return render_template("createaclub.html", user=current_user)
                # return redirect(url_for(".createaclub", club_confirmed=club_password))
                # return redirect("/createaclub")
                return redirect("/")
                
                # return render_template("clubdashboard.html", club_info=Club.query.all(), user_info=User.query.all(), user=current_user)
                # else:
                    # print("Current user is not an advisor.")
                    # flash("Your advisor has to verify your club's code before you can!", "error")
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

    # If the user is not logged in:
    # if current_user is None:
    #     return redirect("/login")
    
    # Otherwise
    return render_template("layout.html", club_info=Club.query.all(), joined_clubs=current_user.clubs, user=current_user)

@views.route("/<id>/join", methods=["GET", "POST"])
def join(id):
    join_club = Club.query.filter_by(id=id).first()
    current_user.clubs.append(join_club)
    db.session.commit()
    flash(f"Successfully joined {join_club.club_name}!", "success")
    return redirect("/")

@views.route("/<id>/leave", methods=["GET", "POST"])
def leave(id):
    print(f"229 - {id}")
    leave_club = Club.query.filter_by(id=id).first()
    current_user.clubs.remove(leave_club)
    db.session.commit()
    flash(f"Successfully left {leave_club.club_name}!", "success")
    return redirect("/")

@views.route("/clubdashboard/<goto>", methods=["GET", "POST"])
@login_required
def club_dashboard(goto):
    print(f"137 - current_user.role = {current_user.role}")
    # Remove a member:
    if goto == "adjust":
        if request.method == "POST":
            change_club_id = request.form.get("changeclubid")
            change_club_name = request.form.get("changeclubname")
            change_president_email = request.form.get("changepresidentemail")
            change_vp_email1 = request.form.get("changevicepresidentemail1")
            change_vp_email2 = request.form.get("changevicepresidentemail2")
            change_vp_email3 = request.form.get("changevicepresidentemail3")
            change_advisor_email = request.form.get("changeadvisoremail")
            change_room_number = request.form.get("changeroomnumber")
            change_club_starttime = request.form.get("changeclubstarttime")
            change_club_days = request.form.getlist("changeclubday")
            change_club_description = request.form.get("changeclubdescription")

            change_club = Club.query.filter_by(secret_password=change_club_id).first()
            if change_club:
                if change_club_name:
                    print(f"Old club name: {change_club.club_name}")
                    change_club.club_name = change_club_name
                    print(f"New club name: {change_club.club_name}")
                    db.session.commit()
                    # flash("Club info changed!", "success")
                    # return redirect("/clubdashboard/info")
                else: print("Failed to change name")
                if change_room_number:
                    change_club.room_number = change_room_number
                    # flash("Club info changed!", "success")
                    db.session.commit()
                if change_club_starttime:
                    change_club.start_time = change_club_starttime
                    # flash("Club info changed!", "success")
                    db.session.commit()
                if change_club_description:
                    change_club.description = change_club_description
                    # flash("Club info changed!", "success")
                    db.session.commit()
                if change_club_days:
                    club_days_final = ""
                    if len(change_club_days) == 1:
                        club_days_final = change_club_days[0]
                    elif len(change_club_days) == 2: 
                        club_days_final += change_club_days[0] + " and " + change_club_days[1]
                    else:
                        for i in range(len(change_club_days)):
                            if i == len(change_club_days) - 2:
                                club_days_final += change_club_days[len(change_club_days) - 2] + " and " + change_club_days[len(change_club_days) - 1]
                                break
                            club_days_final += change_club_days[i] + ", "
                    change_club.club_day = club_days_final
                    # flash("Club info changed!", "success")
                    db.session.commit()
                flash("Club info successfully changed!", "success")
                return redirect("/clubdashboard/info")
            else:
                flash("Club ID not found!", "error")
                return redirect("/clubdashboard/adjust")
            
        return render_template("clubdashboard.html", title="adjust", club_info=Club.query.all(), user_info=User.query.all(), user=current_user, your_clubs=Club.query.filter_by(president_email=current_user.email))
    if goto == "info":
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
    # session["club_confirmed"] = "NO"
    print(f"261 - {request.args.get('club_confirmed')}")
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
        club_days = request.form.getlist("clubday")
        print(f"Days selected: {club_days}")
        club_days_final = ""
        if len(club_days) == 1:
            club_days_final = club_days[0]
        elif len(club_days) == 2: 
            club_days_final += club_days[0] + " and " + club_days[1]
        else:
            for i in range(len(club_days)):
                if i == len(club_days) - 2:
                    club_days_final += club_days[len(club_days) - 2] + " and " + club_days[len(club_days) - 1]
                    break
                club_days_final += club_days[i] + ", "
            
        print(f"Club days final: {club_days_final}")
        new_advisor = User.query.filter_by(email=advisor_email).first()
        if new_advisor:
            new_advisor.role = "Advisor"
            db.session.commit()

        # Making the random password:
        secret_password = random.randint(100, 1000000)
        session["secret_password"] = secret_password
        print(f"Session created: {session['secret_password']}")
        print(f"Secret password: {secret_password}")

        # New club info verification:
        if president_email != current_user.email:
            print(f"Current user email - {current_user.email}. President email - {president_email}")
            flash("Only the president can register their club.", "error")
            return redirect("/createaclub")

        is_unique_club = Club.query.filter_by(club_name=club_name).first()
        if is_unique_club:
            flash("Club name already taken.", "error")
            return redirect("/createaclub")
        
        if advisor_email[0].isnumeric():
            flash("Invalid advisor email.", "error")
            return redirect("/createaclub")

        # Sending the confirmation email to advisor:
        senderemail = "crlsclubfinder@gmail.com"
        senderpassword = "wmzhhaxtzqnvyuze"
        subject = f"{club_name} has submitted you as their club advisor"
        body = f"""Hello! 

{president_email} is signing their club, {club_name}, up to the ClubFinder website. They selected you as their club advisor. If you are not their advisor, please delete this email, or email 25ranjaria@cpsd.us for technical assistance. 

If you are the advisor of {club_name}, please use the code below to confirm both you and your club's identity:

CODE: {secret_password}

Go to clubfinder.com, create an account with this email, and hit "Register Your Club," and type in your club's code. If the code works, your club is all set, and you can give this code to your club's president and vicepresidents. DO NOT GIVE THIS CODE TO CLUB MEMBERS.
If this code doesn't work, please make sure you're logged in with the same email that you received this email on. You should be the only one able to use this code at first. Once you use it once, your club's presidents and vide presidents can use it after you. If the code still doesn't work, please email 25ranjaria@cpsd.us for technical assitance. 

Thank you!
ClubFinder

        """

        send_mail(email_sender=senderemail, email_password=senderpassword, email_receiver=advisor_email, subject=subject, body=body)
        print("Email sent")
        flash("Email successfully sent!")

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
        db.session.commit()
        print(f"President: {president}")
        # Make sure the club president is the person who is currently logged in:
        if president_email == current_user.email:
            print("True")

        new_club = Club(club_name=club_name, president_email=president_email, vicepresident_email1=vicepresident_email1, vicepresident_email2=vicepresident_email2, vicepresident_email3=vicepresident_email3, advisor_email=advisor_email, room_number=room_number, start_time=start_time, description=description, secret_password=secret_password, club_day=club_days_final, status="Pending")
        db.session.add(new_club)
        db.session.commit()

        # This all has to happen only after the advisor confirms the club: 
        # club_name=club_name, president_email=president_email, vicepresident_email1=vicepresident_email1, vicepresident_email2=vicepresident_email2, vicepresident_email3=vicepresident_email3, advisor_email=advisor_email, room_number=room_number, start_time=start_time, description=description, secret_password=secret_password, club_day=club_days_final

    return render_template("createaclub.html", user=current_user)

# Search:
@views.route("/search")
def search():
    # q gets the value of q, which was passed in from the input field from the HTML. 
    q = request.args.get("q")
    print(q)

    if q:
        # If the user types something in, all of the clubs will filter if they have (or contain) the value of q. 
        results = Club.query.filter(Club.club_name.contains(q) | Club.president_email.contains(q)).order_by(Club.club_name.asc()).all()
    else:
        # Else, if there is no value in q, results will be set to every item in the Club class. 
        results = Club.query.all()
    
    return render_template("searchresults.html", results=results, joined_clubs=current_user.clubs)

@views.route("/joinleavebuttons")
def joinleavebuttons():
    return render_template("joinleavebuttons.html", club_info=Club.query.all(), joined_clubs=current_user.clubs, user=current_user)

@views.app_errorhandler(404)
def handle_404(err):
    return render_template("404.html", user=current_user), 404

@views.app_errorhandler(500)
def handle_404(err):
    return render_template("500.html", user=current_user), 500

@views.app_errorhandler(403)
def handle_403(err):
    return render_template("403.html", user=current_user), 403