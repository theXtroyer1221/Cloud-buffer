from cloudBuffer.forms import SearchForm, locationSearch, RegistrationForm, LoginForm, UpdateAccountForm, PostForm, GroupForm, GroupPostForm, AddGroupCommentForm, EditGroupCommentForm, RequestResetForm, ResetPasswordForm, AdminEmailForm, SearchPostForm, MessageForm, AddCommentForm, EditCommentForm, EmptyForm
from flask import render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from cloudBuffer.models import User, Post, Comment, Group, Grouppost, Groupcomment
from cloudBuffer import app, bcrypt, db, mail
from flask_mail import Message
from datetime import datetime

from PIL import Image, ImageOps
import requests
import secrets
import random
import numpy as np
import json
import os

from google_images_search import GoogleImagesSearch

GCS_DEVELOPER_KEY = os.environ.get('GCS_DEVELOPER_KEY')
GCS_CX = os.environ.get('GCS_CX')
IP_STACK = os.environ.get("IP_STACK")


@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        logout_user()
    form = SearchForm()
    location_form = locationSearch()

    if request.args.get("search", None):
        query = request.args["search"]

        return redirect(url_for("search", query=query))

    if request.args.get("hfield", None):
        headers_list = request.headers.getlist("X-Forwarded-For")
        user_ip = headers_list[0] if headers_list else request.remote_addr
        url = 'http://api.ipstack.com/{}?access_key={}'.format(
            "83.250.184.69", IP_STACK)
        r = requests.get(url)
        j = r.json()
        query = j["city"]

        return redirect(url_for("search", query=query))

    return render_template("index.html",
                           form=form,
                           location_form=location_form,
                           data="data")


@app.route("/weather/<query>")
def search(query):
    if current_user.is_authenticated:
        logout_user()
    form = SearchForm()
    location_form = locationSearch()

    if request.args.get("search", None):
        query = request.args["search"]

        return redirect(url_for("search", query=query))

    if request.args.get("hfield", None):
        headers_list = request.headers.getlist("X-Forwarded-For")
        user_ip = headers_list[0] if headers_list else request.remote_addr
        url = 'http://api.ipstack.com/{}?access_key={}'.format(
            "12.32.32.11", IP_STACK)
        r = requests.get(url)
        j = r.json()
        query = j["city"]

        return redirect(url_for("search", query=query))

    payload = {
        'q': query,
        'units': 'metric',
        'appid': 'd4783db24d0d806b60afb366ceea4d7e'
    }
    r = requests.get('http://api.openweathermap.org/data/2.5/weather',
                     params=payload)
    data = r.json()

    if data["cod"] == 200:
        search_country = data["sys"]["country"]
        search_query = f"{query} city {search_country}"

        gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)
        _google_search_params = {
            'q': search_query,
            'num': 1,
            'safe': 'off',
            'imgSize': 'xlarge'
        }
        try:
            gis.search(search_params=_google_search_params)
        except:
            img = "../static/images/notfound.jpg"

        img = "../static/images/notfound.jpg"

        for image in gis.results():
            img = image.url

        return render_template("search.html",
                               query=query,
                               data=data,
                               form=form,
                               location_form=location_form,
                               img=img)
    else:
        return render_template("search.html",
                               query=query,
                               data=data,
                               form=form,
                               location_form=location_form)

@app.route("/blog",  methods=['GET', 'POST'])
def blog():
    with open("cloudBuffer/message.json", "r") as f:
        message = json.load(f)
    form = SearchPostForm()
    page = request.args.get("page", 1, type=int)
    if current_user.is_authenticated:
        image_file = url_for("static",
                             filename="profile_pics/" +
                             current_user.image_file)
    else:
        image_file = None
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=5)
    if form.validate_on_submit():
        post_query = Post.query.filter_by(title=form.search.data).first()
        if post_query:
            return redirect(url_for('post', post_id=post_query.id))
        else:
            flash(f"No article found with the name {form.search.data}", "danger")
            return redirect(url_for("blog"))
    return render_template("blog.html", data="data", title="Blog", image_file=image_file, posts=posts, form=form, message=message)

@app.route('/posts')
def posts_json():
	res = Post.query.all()
	list_posts = [r.as_dict() for r in res]
	return jsonify(list_posts)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("blog"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(
                url_for("blog"))
        else:
            flash('Login Unsuccessful. Please check email and password',
                  'danger')

    return render_template("login.html",
                           form=form,
                           data="data",
                           title="Log in",
                           post="post")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("blog"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f'Your account has been created, you are now able to log in, {form.username.data}',
            'success')
        return redirect(url_for('login'))

    return render_template("signup.html",
                           form=form,
                           data="data",
                           title="Sign up",
                           post="post")


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics",
                                picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.resize(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.biography = form.biography.data
        db.session.commit()
        flash("Account information has been updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.biography.data = current_user.biography
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template("account.html",
                           title="Account",
                           image_file=image_file,
                           form=form)


@app.route("/user/<username>", methods=['GET', 'POST'])
def user(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    if current_user == user:
        return redirect(url_for("account"))
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user.html",
                           title=user.username,
                           user=user,
                           posts=posts,
                           post="post")


def send_admin_mail(title, body, recipients=None):
    if recipients == None:
        users = [user.email for user in User.query.all()]
    else:
        users = [recipients]
    msg = Message(f"{title} - CloudBuffer", recipients=users)
    msg.html = render_template("admin_email.html", body=body)
    mail.send(msg)


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    form = AdminEmailForm()
    messageForm = MessageForm()
    if not current_user.admin:
        abort(403)
    if form.identifier.data == 'form' and form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        send_admin_mail(title, body)
    if messageForm.identifier.data == 'messageForm' and messageForm.validate_on_submit():
        content = messageForm.content.data
        print(content)
        with open("cloudBuffer\message.json", "w") as f:
            content_obj = {"content": content}
            data = json.dump(content_obj, f, indent=4)
        flash("Success! The blog page has been updated with the message", "success")
    return render_template("dashboard.html",
                           title="Admin dashboard - Cloudbuffer",
                           User=User,
                           Post=Post,
                           form=form, messageForm=messageForm)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    image_file = url_for("static",
                         filename="profile_pics/" + current_user.image_file)
    form = PostForm()
    if form.validate_on_submit():
        post = Post(id=random.randint(1000, 9999),
                    title=form.title.data,
                    content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("The post has been created successfully", "success")
        return redirect(url_for("blog"))
    return render_template('create_post.html',
                           title="New post",
                           form=form,
                           image_file=image_file,
                           legend="Create a post")

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    form = AddCommentForm()
    editform = EditCommentForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
    commentformplaceholder = "placeholder"
    return render_template("post.html",
                           title=post.title,
                           post=post,
                           data="post_site", Post=Post, form=form, editform=editform, commentformplaceholder=commentformplaceholder, grouppost=False)

@app.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash("Your comment has been deleted", "success")
    return redirect(url_for("post", post_id=comment.post_id))

@app.route("/comment/<int:comment_id>/update", methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    editform = EditCommentForm()
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        if not current_user.admin:
            abort(403)
    if editform.validate_on_submit():
        comment.content = editform.content.data
        db.session.commit()
    flash("Your comment has been updated", "success")
    return redirect(url_for("post", post_id=comment.post_id))

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        if not current_user.admin:
            abort(403)
        else:
            pass
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated", "success")
        return redirect(url_for("post", post_id=post.id))
    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',
                           title="Update existing post",
                           legend="Update an existing post",
                           form=form)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        if not current_user.admin:
            abort(403)
    if current_user.admin:
        title = "Your post has been deleted"
        body = f"Your post ({post.title}) has been removed by the admins from our website. This can be the cause of violating the terms of posting in our website where the post could have included directly or indirectly Profanity, Abusive Content, Adult Content, Illegal Content, Offensive Content and/or Threats. Please respect the action taken by admins. The post has been only removed without any warning. You are still free to post on the website. For more question feel free to contact us."
        send_admin_mail(title, body, post.author.email)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", "success")
    return redirect(url_for("blog"))

def save_group_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics",
                                picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.resize(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/group/new", methods=['GET', 'POST'])
@login_required
def new_group():
    image_file = url_for("static",
                         filename="profile_pics/" + current_user.image_file)
    form = GroupForm()
    if form.validate_on_submit():
        title_name = form.title.data.replace(" ", "_").lower()
        group_picture = save_group_pic(form.picture.data)
        group = Group(id=random.randint(1000, 99999),
                    title=title_name,
                    description=form.description.data,
                    language=form.language.data,)
        db.session.add(group)
        db.session.commit()
        group.image_file = group_picture 
        db.session.commit()
        flash("The group has been created successfully", "success")
        return redirect(url_for("group", title=group.title))
    return render_template('create_group.html',
                           title="New group",
                           form=form,
                           image_file=image_file,
                           legend="Create a new group", data="post_site")

@app.route("/group/<title>", methods=['GET', 'POST'])
def group(title):
    group = Group.query.filter_by(title=title).first_or_404()
    grp_img = url_for("static",
                    filename="profile_pics/" + group.image_file)
    form = GroupPostForm()
    null_form = EmptyForm()
    #page = request.args.get("page", 1, type=int)
    posts = Grouppost.query.filter_by(group_id=group.id).all()
    return render_template("group_page.html",
                           title=group.title,
                           group=group,
                           post="post", group_img=grp_img, data="post_site", form=form, posts=posts, empty_form=null_form)

@app.route("/group/<title>/post/new", methods=['GET', 'POST'])
@login_required
def group_post_new(title):
    group = Group.query.filter_by(title=title).first_or_404()
    grp_img = url_for("static",
                    filename="profile_pics/" + group.image_file)
    form = GroupPostForm()
    if form.validate_on_submit():
        post = Grouppost(id=random.randint(1000, 99999),
                    title=form.title.data,
                    content=form.content.data,
                    user_id=current_user.id,
                    group_id=group.id)
        db.session.add(post)
        db.session.commit()
        flash("The post has been created successfully", "success")
        return redirect(url_for("group", title=group.title))
    return render_template("create_group_post.html",
                           title=group.title,
                           group=group,
                           post="post", group_img=grp_img, data="post_site", form=form, legend="Create a group post")

@app.route("/group/<title>/<int:post_id>", methods=['GET', 'POST'])
def group_post(title, post_id):
    form = AddGroupCommentForm()
    editform = EditGroupCommentForm()
    grouppost = Grouppost.query.get_or_404(post_id)
    if form.validate_on_submit():
        groupcomment = Groupcomment(id=random.randint(1000, 99999),
                    content=form.content.data,
                    author=current_user, 
                    post=grouppost)
        db.session.add(groupcomment)
        db.session.commit()
    commentformplaceholder = "placeholder"
    return render_template("post.html",
                           title=grouppost.title,
                           post=grouppost,
                           data="post_site", Post=Post, form=form, editform=editform, commentformplaceholder=commentformplaceholder, grouppost=True)

@app.route("/groupcomment/<int:comment_id>/update", methods=['GET', 'POST'])
@login_required
def edit_group_comment(comment_id):
    editform = EditCommentForm()
    comment = Groupcomment.query.get_or_404(comment_id)
    if comment.author != current_user:
        if not current_user.admin:
            abort(403)
    if editform.validate_on_submit():
        comment.content = editform.content.data
        db.session.commit()
    find_post = comment.post_id
    group = Grouppost.query.get_or_404(find_post)
    flash("Your comment has been updated", "success")
    return redirect(url_for("group_post", title=group.author.title, post_id=comment.post_id))

@app.route("/groupcomment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_group_comment(comment_id):
    comment = Groupcomment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    find_post = comment.post_id
    group = Grouppost.query.get_or_404(find_post)
    flash("Your comment has been deleted", "success")
    return redirect(url_for("group_post", title=group.author.title, post_id=comment.post_id))

@app.route('/follow/<title>', methods=['GET', 'POST'])
@login_required
def follow(title):
    form = EmptyForm()
    if form.validate_on_submit():
        group = Group.query.filter_by(title=title).first()
        if group is None:
            flash('The group "{}" was not found.'.format(title))
            return redirect(url_for('blog'))
        if current_user in group.users:
            flash('You are already following this group!', "warning")
            return redirect(url_for('group', title=title))
        current_user.follow(group)
        db.session.commit()
        flash('You have successfully joined {}!'.format(title), "success")
        return redirect(url_for('group', title=title))
    else:
        return redirect(url_for('blog'))

@app.route('/unfollow/<title>', methods=['POST'])
@login_required
def unfollow(title):
    form = EmptyForm()
    if form.validate_on_submit():
        group = Group.query.filter_by(title=title).first()
        if group is None:
            flash('The group "{}" was not found.'.format(title), "danger")
            return redirect(url_for('blog'))
        current_user.unfollow(group)
        db.session.commit()
        flash('You have unfollowed {}'.format(title), "success")
        return redirect(url_for('group', title=title))
    else:
        return redirect(url_for('blog'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request - CloudBuffer",
                  sender="noreply@CloudBuffer.com",
                  recipients=[user.email])
    msg.html = render_template("email.html",
                               user=user,
                               url=url_for('reset_token',
                                           token=token,
                                           _external=True))
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("blog"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password",
            "info")
        return redirect(url_for("login"))
    return render_template('reset_request.html',
                           title='Reset Password',
                           form=form,
                           post="post")


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("blog"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(
            f'Your password has been updated, You are now able to log in with your new password',
            'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html',
                           title='Reset Password',
                           form=form,
                           post="post")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("blog"))

@app.route("/terms")
def terms():
    return render_template('terms.html', data="data")


@app.errorhandler(404)
def page_not_found(e):
    data = 404
    return render_template('error.html',
                           e=e,
                           h1="404",
                           data=data,
                           title="Page not found"), 404


@app.errorhandler(403)
def forbidden(e):
    data = 403
    return render_template('error.html',
                           e=e,
                           h1="Whoa! Staff only!",
                           data=data,
                           title="Page not accessible"), 403


@app.errorhandler(500)
def general_server_problem(e):
    data = 500
    return render_template('error.html',
                           e=e,
                           h1="Opps! Something went wrong (500)",
                           data=data,
                           title="Page not accessible"), 500
