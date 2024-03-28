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

findamentor = Blueprint("findamentor", __name__)

@findamentor.route("/findamentor", methods=["GET", "POST"])
def findamentor_home():
    return render_template("findamentor.html", user=current_user)