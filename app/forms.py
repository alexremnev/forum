from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, DataRequired

from app.services import userService


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=1, max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=50)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), DataRequired(), Length(min=1, max=30)])
    email = StringField('email',
                        validators=[InputRequired(), DataRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=100)])

    def validate(self):
        form = FlaskForm.validate(self)
        if not form:
            return False

        user = userService.get_by_username(self.username.data)
        if user is not None:
            self.username.errors.append('Nickname already exists')
            return False

        user = userService.get_by_email(self.email.data)
        if user is not None:
            self.email.errors.append('Email already exists')
            return False
        return True


class PostForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=1, max=50)])
    body = TextAreaField('body', validators=[InputRequired(), Length(max=5000)])


class CommentForm(FlaskForm):
    text = StringField('text:', validators=[InputRequired(), Length(min=1, max=200)])
