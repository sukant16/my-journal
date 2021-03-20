from flask import Blueprint

users_bp = Blueprint('users', __name__)
posts_bp = Blueprint('posts', __name__)

from app.api import posts, users, errors
