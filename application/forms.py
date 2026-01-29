from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from application.models import User 

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6, max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6, max=30)])
    password_confirmed = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=30),EqualTo('password')])
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=1, max=55)])
    last_name = StringField("Last Name", validators=[DataRequired(),Length(min=1,max=55)])
    submit = SubmitField("Register Now")

    def validate_email(self,email):
        user = User.objects(email=email.data).first()  # query mongoengine for existing email
        #user_all = User.objects(email=email.data).all()
        #print('User: ',user,'/n')
        #print('user_all: ',user, '/n')
        if user:
            raise ValidationError("Email is already in use, pick another one.")
        

    