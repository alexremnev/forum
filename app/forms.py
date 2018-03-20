from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length


class PostForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=1, max=50)])
    body = TextAreaField('body', validators=[InputRequired(), Length(max=5000)])


class CommentForm(FlaskForm):
    text = StringField('text:', validators=[InputRequired(), Length(min=1, max=200)])
