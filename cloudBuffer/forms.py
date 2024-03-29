from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, SubmitField, HiddenField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from cloudBuffer.models import User, Post, Group


class SearchForm(FlaskForm):
    search = StringField("search")
    submit = SubmitField("submit")


class locationSearch(FlaskForm):
    hfield = HiddenField("hfield")
    location_submit = SubmitField()


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(),
                                        EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is already taken, please choose another one")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "There is already an account with that email")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    biography = TextAreaField("Biography", validators=[Length(min=5, max=150)])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is already taken, please choose another one"
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "There is already an account with that email")


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")

class SearchPostForm(FlaskForm):
    search = StringField("Title", validators=[DataRequired()])
    submit = SubmitField("Search")

class AddCommentForm(FlaskForm):
    content = StringField("Content", validators=[DataRequired(), Length(min=5, max=140)])
    submit = SubmitField("Post")

class EditCommentForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=5, max=140)])
    submit = SubmitField("Edit")   

from cloudBuffer.languages import language_list
class GroupForm(FlaskForm):
    title = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=100)])
    language = SelectField('Language', choices=language_list)
    picture = FileField('Group profile picture',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Create group')

    def validate_title(self, title):
        group = Group.query.filter_by(title=title.data).first()
        if group:
            raise ValidationError(
                "That group title is already taken, please choose another one")


class UpdateGroupForm(FlaskForm):
    title = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=100)])
    language = SelectField('Language', choices=language_list)
    image_file = FileField('Group profile picture',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Save changes')

    def validate_title(self, title):
        group = Group.query.filter_by(title=title.data).first()
        if group:
            raise ValidationError(
                "That group title is already taken, please choose another one")

class AddAdminForm(FlaskForm):
    username = StringField("User's Username", validators=[DataRequired()])
    submit = SubmitField("Send")

class GroupPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")
class AddGroupCommentForm(FlaskForm):
    content = StringField("Content", validators=[DataRequired(), Length(min=5, max=140)])
    submit = SubmitField("Post")
class EditGroupCommentForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=5, max=140)])
    submit = SubmitField("Edit")   
class AdminEmailForm(FlaskForm):
    identifier = StringField()
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField("Send")

class MessageForm(FlaskForm):
    identifier = StringField()
    content = TextAreaField('Content')
    send = SubmitField("Send")

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                "There is no account with that email. You must register first."
            )

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(),
                                        EqualTo('password')])
    submit = SubmitField("Reset password")
