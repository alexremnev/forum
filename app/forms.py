from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=1, max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=50)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=1, max=30)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=50)])
