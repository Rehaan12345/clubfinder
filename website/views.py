from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from .models import User, Club, Info
from .sendmail import send_mail
from . import db
import random
import smtplib
from flask_mail import Mail, Message
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_session import Session
import datetime
from .allinfo import PFInfo

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form.get("addtitle")
        body = request.form.get("addbody")
        add_info = Info(title=title, body=body, subheader="Rehaan")
        db.session.add(add_info)
        db.session.commit()
        flash("Added new info!")

    return render_template("layout.html", user=current_user, info=Info.query.all())

@views.route("/removetext/<id>", methods=["GET", "POST"])
def remove_text(id):
    remove_text = Info.query.filter_by(text_id=id).first()
    db.session.delete(remove_text)
    db.session.commit()
    flash("Successfully deleted")
    return redirect("/")

@views.app_errorhandler(404)
def handle_404(err):
    return render_template("404.html", user=current_user), 404

@views.app_errorhandler(500)
def handle_404(err):
    return render_template("500.html", user=current_user), 500

@views.app_errorhandler(403)
def handle_403(err):
    return render_template("403.html", user=current_user), 403