from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Club, Links
from werkzeug.security import generate_password_hash, check_password_hash 
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .sendmail import send_mail, send_alt_mail
from .forms import LoginForm, SignupForm

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"]) 
def login():
    form = LoginForm()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            user = User.query.filter_by(email=email).first() # Filters all of the users who have this email.
            if user: # If this user is found: 
                if check_password_hash(user.password, password): # Checks this user's password.
                    flash(f"Successfully logged in as {user}", category="success")
                    login_user(user, remember=True) # Logs in the user. Remembers the fact that this user is logged in until the user clears their browser history / session. Will be stored in the flask webserver - until the webserver restarts. 
                    return redirect("/")
                    # return render_template("layout.html", club_info=Club.query.all(), joined_clubs=current_user.clubs, user=current_user)
                else:
                    flash("Incorrect password, try again!", category="error")
            else: # If this user is not found:
                flash("This email does not belong to an account. Try creating a new account!", category="error")

        submit = request.form.get("loginasguest")
        print(f"20 - {submit}") 

        if submit == "Login as Guest":
            print("33 - ok")
            guest_user = User.query.filter_by(email="25guestuser123@cpsd.us").first()
            if guest_user:
                print("Found the guest user.")
                login_user(guest_user, remember=True)
                flash(f"Successfully logged in as {guest_user}", "success")
                return redirect("/")
            else:
                print("No guest user found!")
        else:
            print("DIdn't register logging in as a guest.")

    return render_template("login.html", user=current_user, name="auth", form=form, links=Links.query.all())

def check_email(email):
    ind_at = email.index("@")
    rest = email[ind_at:]
    try:
        if rest.index("cpsd.us") > 0:
            return True
        return False
    except:
        return False

@auth.route("/signup", methods=["GET", "POST"]) 
def signup(): 
    form = SignupForm()

    if request.method == "POST":
        email = request.form.get("email")
        if not check_email(email):
            flash("Email needs to be a cpsd email.", "error")
            return redirect("/signup")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password") 
        role = "Member"
        if email[0].isnumeric():
            role = "Member"
        else: role = "Advisor"

        # Makes sure two users don't use the same email address: 
        user = User.query.filter_by(email=email).first() 
        if user: 
            flash("This email is already linked to an account!", category="error") 
        elif len(email) < 4: 
            flash("Your email must be greater than 3 characters!", category="error")
        elif password != confirm_password:
            flash("Your passwords do not match!", category="error") 
        elif len(password) < 7:
            flash("Your password must be greater than 6 characters!", category="error")
        else:
            new_user = User(email=email, password=generate_password_hash(password, method="sha256"), is_leader=False, role=role)
            db.session.add(new_user) 
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Your account has been created!", category="success")
            return redirect("/")

    return render_template("signup.html", user=current_user, name="auth", form=form, links=Links.query.all())

@auth.route("/logout") 
@login_required # Makes sure we cannot access this route / page unless the user is logged in - can't logged out if not logged in.  
def logout():
    logout_user() # Logs out the current user. 
    flash("Logged out", category="success")
    return redirect(url_for("auth.login"))

@auth.route("/<id>/<stage>/forgotpassword", methods=["GET", "POST"])
def forgot_password(id, stage):
    if stage == "email":
        if request.method == "POST":
            email = request.form.get("email")
            user = User.query.filter_by(email=email).first()
            if user:
                email_sender = "crlsclubfinder@gmail.com"
                email_password = "wmzhhaxtzqnvyuze"
                email_receiver = email
                subject = "Change ClubFinder Pasword"
                text = f"Follow this link to change your password: https://www.crlsclubfinder.com/{user.id}/changepassword/"
                html = f"""
<h2>Change Password</h2>
<p>Click the button below to change your password</p>
<button class="clubbutton" type="submit"><a href='https://www.crlsclubfinder.com/{user.id}/changepass/forgotpassword'>Change Password</a></button>
"""
                send_alt_mail(email_sender=email_sender, email_password=email_password, email_receiver=email_receiver, subject=subject, text=text, html=html)
                flash("Email successfully sent!", "success")
            else:
                flash("This email is not linked with an account.", "error")
                return redirect("/forgotpassword/email")
        return render_template("forgotpassword.html", user=current_user, stage=stage, links=Links.query.all())
    
    if stage == "changepass":
        if request.method == "POST":
            id = request.form.get("id")
            user = User.query.filter_by(email=id).first()
            if user is not None:
                id = user.id
                print(f"121 - {id}")
                new_password = request.form.get("newpassword")
                confirm_new_password = request.form.get("confirm-newpassword")
                if new_password != confirm_new_password:
                    flash("Passwords don't match.", "error")
                    return redirect("/changepass/forgotpassword")
                new_password = generate_password_hash(new_password, method="sha256")
                print(f"128 Old Pass - {user.password}")
                user.password = new_password
                db.session.commit()
                print(f"131 New Pass - {user.password}")
                flash("Successfully changed password!", "success")
                return redirect("/login")
            else: flash("No user")
        return render_template("forgotpassword.html", user=current_user, stage=stage, id=id, links=Links.query.all())
        
        # Find and change this password. 
    
    return render_template("forgotpassword.html", user=current_user, stage=stage, links=Links.query.all())

@auth.route("/<id>/changepassword", methods=["GET", "POST"])
def changepass(id):
    return redirect("/id/forgotpassword")
    # return redirect(url_for("auth.forgot_password", stage="changepass"))