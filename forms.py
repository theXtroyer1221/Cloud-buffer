from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField


class SearchForm(FlaskForm):
    search = StringField("search")
    submit = SubmitField("submit")


class locationSearch(FlaskForm):
    hfield = HiddenField("hfield")
    location_submit = SubmitField()