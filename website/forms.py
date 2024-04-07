from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, SelectMultipleField, widgets, IntegerField, TimeField, TextAreaField
from wtforms.validators import DataRequired

# Making the checkbox:
class MultiCheckboxField(SelectMultipleField): # Source: https://gist.github.com/doobeh/4668212 
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# Signup form for mentors
class MentorSignupForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired()], render_kw={"placeholder": "Rehaan"})
    lastname = StringField("Last Name", validators=[DataRequired()], render_kw={"placeholder": "Anjaria"})
    dob = DateField("Birthday", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()], render_kw={"placeholder": "25ranjaria@cpsd.us"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password123!"})
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired()], render_kw={"placeholder": "password123!"})
    mentormentee = RadioField("Are you signing up as a Mentor or Mentee?", choices=[("Mentor"), ("Mentee")])
    race = MultiCheckboxField("Race", choices=[("Asian / South Asian"), ("Black"), ("Hispanic"), ("White")])
    religion = MultiCheckboxField("Religion", choices=[("Christian"), ("Muslim"), ("Jewish"), ("Hindu"), ("N/A")])
    gender = RadioField("Gender", choices=[("Male"), ("Female"), ("Non-Binary")])
    languages = MultiCheckboxField("Languages", choices=[("Amharic"), ("Bangla"), ("Spanish"), ("Hindi"), ("Portuguese"), ("Chinese")])
    academics = MultiCheckboxField("Academics", choices=[("English"), ("History"), ("Chemistry"), ("Physics"), ("Biology"), ("Computer Science")])
    submit = SubmitField("Log In")

# Login Signup form:
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()], render_kw={"placeholder": "25ranjaria@cpsd.us"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "password123!"})
    submit = SubmitField("Log In")

# Regular Signup form:
class SignupForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()], render_kw={"placeholder": "25ranjaria@cpsd.us"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "password123!"})
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Sign Up")

class RegisterClub(FlaskForm):
    clubname = StringField("Club Name", validators=[DataRequired()], render_kw={"placeholder": "Club 1"})
    presidentemail = StringField("President Email", validators=[DataRequired()], render_kw={"placeholder": "president@cpsd.us"})
    vicepresidentemail1 = StringField("Vice President Email", render_kw={"placeholder": "vicepresident@cpsd.us"})
    vicepresidentemail2 = StringField("Vice President Email", render_kw={"placeholder": "vicepresident@cpsd.us"})
    vicepresidentemail3 = StringField("Vice President Email", render_kw={"placeholder": "vicepresident@cpsd.us"})
    advisoremail = StringField("Advisor Email", validators=[DataRequired()], render_kw={"placeholder": "advisor@cpsd.us"})
    roomnumber = IntegerField("Room Number", validators=[DataRequired()], render_kw={"placeholder": "1234"})
    clubstarttime = TimeField("Club Start Time", validators=[DataRequired()])
    clubday = MultiCheckboxField("Select which day(s) your club meets", choices=[("Monday"), ("Tuesday"), ("Wednesday"), ("Thursday"), ("Friday")])
    clubdescription = TextAreaField("Club Description", validators=[DataRequired()], render_kw={"palceholder": "This is a great club. You should join!"})
    submit = SubmitField("Confirm")

class AdjustClub(FlaskForm):
    clubid = IntegerField("Club ID", validators=[DataRequired()], render_kw={"placeholder": "123456789"})
    changeclubname = StringField("Club Name", render_kw={"placeholder": "Club 1"})
    changepresidentemail = StringField("President Email", render_kw={"placeholder": "president@cpsd.us"})
    changevicepresidentemail1 = StringField("Vice President Email", render_kw={"placeholder": "vicepresident@cpsd.us"})
    changevicepresidentemail2 = StringField("Vice President Email", render_kw={"placeholder": "vicepresident@cpsd.us"})
    changevicepresidentemail3 = StringField("Vice President Email", render_kw={"placeholder": "vicepresident@cpsd.us"})
    changeadvisoremail = StringField("Advisor Email", render_kw={"placeholder": "advisor@cpsd.us"})
    changeroomnumber = IntegerField("Room Number", render_kw={"placeholder": "1234"})
    changeclubstarttime = TimeField("Club Start Time")
    changeclubday = MultiCheckboxField("Select which day(s) your club meets", choices=[("Monday"), ("Tuesday"), ("Wednesday"), ("Thursday"), ("Friday")])
    changeclubdescription = TextAreaField("Club Description", render_kw={"palceholder": "This is a great club. You should join!"})
    submit = SubmitField("Confirm")