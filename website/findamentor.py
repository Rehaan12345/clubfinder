from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from .models import User, Club, Mentor, Links
from .sendmail import send_mail
from . import db
import random
import smtplib
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_session import Session
import datetime 
from .forms import MentorSignupForm

findamentor = Blueprint("findamentor", __name__)

def combining(str):
        final_str = ""
        if len(str) == 1:
            final_str = str[0]
        # elif len(str) == 2: 
        #     final_str += str[0] + " and " + str[1]
        else:
            for i in range(len(str)):
                if i == len(str) - 2:
                    final_str += str[len(str) - 2] + " and " + str[len(str) - 1]
                    break
                final_str += str[i] + " "
            ind_and = final_str.index("and")
            # final_str = final_str[:ind_and]
        return final_str

@findamentor.route("/becomeamentor/<step>", methods=["GET", "POST"])
def becomeamentor(step):
    form = MentorSignupForm()

    # Default values:
    first_name = ""
    last_name = ""
    date_of_birth = ""
    email = ""
    mentormentee = ""
    race = ""
    religion = ""
    gender = ""
    languages = ""
    academics = ""

    if step == "basicinfo":
        if form.validate_on_submit:
            return render_template("becomeamentor.html", step="basicinfo", form=form, user=current_user, links=Links.query.all())
    
    elif step == "morespecific":
        if form.validate_on_submit:
            first_name = form.firstname.data
            last_name = form.lastname.data
            # date_of_birth = form.dob.data
            email = form.email.data
            password = form.password.data
            confirmpassword = form.confirmpassword.data
            if password != confirmpassword:
                flash("Passwords don't match!", "error")
                return redirect("/becomeamentor/basicinfo")
            print(f"firstname - {first_name} lastname - {last_name} email - {email} password - {password}")
            # Creates the user the first time.
            # users.insert_one({"firstname": first_name, "lastname": last_name, "email": email, "mentormentee": mentormentee, "password": password, "race": race, "religion": religion, "gender": gender, "languages": languages, "academics": academics})
            new_mentor = Mentor(firstname=first_name, lastname=last_name, email=email, race=race, religion=religion, gender=gender, languages=languages, academics=academics)
            db.session.add(new_mentor)
            db.session.commit()
            return render_template("becomeamentor.html", step="morespecific", email=email, form=form, user=current_user, links=Links.query.all())
    
    elif step == "confirm":
        if request.method == "POST":
            mentormentee = form.mentormentee.data
            race = form.race.data
            religion = form.religion.data
            gender = form.gender.data
            languages = form.languages.data
            academics = form.academics.data
            email = form.email.data
            # password = request.form.get("password") # Also have to add the confirm password verification.
            print(f"72 - {email}")
            race = combining(race)
            religion = combining(religion)
            languages = combining(languages)
            academics = combining(academics)
            print(f"77 - mentormentee - {mentormentee} race - {race} religion - {religion} gender - {gender} languages - {languages} academics - {academics}")
            # users.update_one({"email": email}, {"$set": {"mentormentee": mentormentee}})
            # users.update_one({"email": email}, {"$set": {"race": race}})
            # users.update_one({"email": email}, {"$set": {"religion": religion}})
            # users.update_one({"email": email}, {"$set": {"gender": gender}})
            # users.update_one({"email": email}, {"$set": {"languages": languages}})
            # users.update_one({"email": email}, {"$set": {"academics": academics}})
            # users.update_one({"email": email}, {"$set": {"password": password}})
            return render_template("becomeamentor.html", step="confirm", mentormentee=mentormentee, race=race, religion=religion, gender=gender, languages=languages, academics=academics, form=form, user=current_user, links=Links.query.all())
        
    elif step == "finish":
        if request.method == "POST":
            # NEED TO Upload all into DB (try catch, etc)
            print(f"firstname - {first_name}, lastname - {last_name}, email - {email}, mentormentee - {mentormentee}, race - {race}, religion - {religion}, gender - {gender}, languages - {languages}, academics - {academics}")
            # users.insert_one({"firstname": first_name, "lastname": last_name, "dob": date_of_birth, "email": email, "mentormentee": mentormentee, "race": race, "religion": religion, "gender": gender, "languages": languages, "academics": academics})
            print("66 - successfully confirmed")
            flash("Account successfully created")
            return render_template("becomeamentor.html", step="finish", form=form, user=current_user, links=Links.query.all())
                
    return render_template("becomeamentor.html", step="basicinfo", form=form, user=current_user, links=Links.query.all())