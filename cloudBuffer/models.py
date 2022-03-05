from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from cloudBuffer import db, login_manager, app
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_group = db.Table(
    'user_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

mod_group = db.Table(
    'mod_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20),
                           nullable=False,
                           default="default.jpg")
    biography = db.Column(db.Text, nullable=True)
    posts = db.relationship("Post", backref="author", lazy=True)
    groupposts = db.relationship("Grouppost", backref="group_author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)
    groupcomments = db.relationship("Groupcomment", backref="author", lazy=True)
    admin = db.Column(db.Boolean(), default=False)

    def follow(self, group):
        if self not in group.users:
            group.users.append(self)

    def unfollow(self, group):
        if self in group.users:
            group.users.remove(self)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    __searchable__ = ['title', "content"]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String())
    comments = db.relationship("Comment", backref="post", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def as_dict(self):
        return {'type': 'post', 'id': self.id, 'title': self.title}

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.timestamp}')"
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.Text, nullable=True)
    image_file = db.Column(db.String(20),
                           nullable=False,
                           default="default.jpg")
    language = db.Column(db.String(), default="International")
    users = db.relationship("User", secondary=user_group, backref=db.backref("groups", lazy='dynamic'))
    moderators = db.relationship("User", secondary=mod_group, backref=db.backref("mod_groups", lazy='dynamic'))
    posts = db.relationship("Grouppost", backref="author", lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Group('{self.title}', '{len(self.users)}')"

    def as_dict(self):
        return {'type': 'group', 'id': self.id, 'title': self.title, 'image': self.image_file}

class Grouppost(db.Model):
    __searchable__ = ['title', "content"]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String())
    comments = db.relationship("Groupcomment", backref="post", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    group_id =  db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)

    def __repr__(self):
        return f"GroupPost('{self.title}', '{self.date_posted})"

    def as_dict(self):
        return {'id': self.id, 'title': self.title}

class Groupcomment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("grouppost.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.timestamp}')"