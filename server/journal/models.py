from datetime import datetime

from flask import url_for
from flask_login import UserMixin

from server.journal import db
from server.journal import login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(64), index =True, unique=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    picture = db.Column(db.String(1000))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self, include_email=False, include_picture=False):
        data = {
            "id": self.id,
            "username": self.username,
            "picture" : self.picture,
            "_links": {
                "self": url_for("users.get_user", id=self.id),
            },
        }
        if include_email:
            data["email"] = self.email
        return data

    def from_dict(self, data):
        for field in ["username", "email", "google_id", "picture"]:
            if field in data:
                setattr(self, field, data[field])


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    post_gdrive_name = db.Column(db.String(50))
    post_gdrive_id = db.Column(db.String(100))
    creation_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<Post {self.post}>"

    def to_dict(self):
        data = {
            "id": self.id,
            "post_gdrive_name": self.post_gdrive_name,
            "post_gdrive_id": self.post_gdrive_id,
            "creation_date": self.creation_date,
            "last_modified": self.last_modified,
        }
        return data

    def from_dict(self, data):
        for field in ["user_id", "last_modified", "post_gdrive_id", "post_gdrive_name"]:
            if field in data:
                setattr(self, field, data[field])
        # if new_post:
        #     setattr(self, 'creation_date', data['creation_date'])
