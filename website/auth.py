from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Club
from werkzeug.security import generate_password_hash, check_password_hash 
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"]) 
def login():
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

    return render_template("login.html", user=current_user, name="auth")

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
    if request.method == "POST":
        email = request.form.get("email")
        if not check_email(email):
            flash("Email needs to be a cpsd email.", "error")
            return redirect("/signup")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password") 
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
            # return render_template("layout.html", club_info=Club.query.all(), joined_clubs=current_user.clubs, user=current_user)

    return render_template("signup.html", user=current_user, name="auth")

@auth.route("/logout") 
@login_required # Makes sure we cannot access this route / page unless the user is logged in - can't logged out if not logged in.  
def logout():
    logout_user() # Logs out the current user. 
    flash("Logged out", category="success")
    return redirect(url_for("auth.login"))