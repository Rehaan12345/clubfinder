from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, SelectMultipleField, widgets
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