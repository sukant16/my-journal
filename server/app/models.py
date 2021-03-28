from datetime import datetime

from flask import url_for

from server.app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    picture = db.Column(db.String(1000))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self, include_email=False, include_picture=False):
        data = {
            'id': self.id,
            'username': self.username,
            '_links': {
                'self': url_for('users.get_user', id=self.id),
            }
        }
        if include_email:
            data['email'] = self.email
        if include_email:
            data['picture'] = self.picture
        return data

    def from_dict(self, data):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    post_gdrive_name = db.Column(db.String(50))
    post_gdrive_id = db.Column(db.String(100))
    creation_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Post {self.post}>'

    def to_dict(self):
        data = {
            'id': self.id,
            'post_gdrive_name': self.post_gdrive_name,
            'post_gdrive_id': self.post_gdrive_id,
            'creation_date': self.creation_date,
            'last_modified': self.last_modified
        }
        return data

    def from_dict(self, data):
        for field in ['post_filename', 'user_id', 'last_modified']:
            if field in data:
                setattr(self, field, data[field])
        # if new_post:
        #     setattr(self, 'creation_date', data['creation_date'])
