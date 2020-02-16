from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SignUpForm(FlaskForm):
    search = StringField("search")
    submit = SubmitField("submit")
    location_submit = SubmitField("submit")