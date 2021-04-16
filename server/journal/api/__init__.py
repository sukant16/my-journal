from flask import Blueprint

users_bp = Blueprint("users", __name__)
posts_bp = Blueprint("posts", __name__)
auth_bp = Blueprint("auth", __name__)


from server.journal.api import posts, users, errors, auth
