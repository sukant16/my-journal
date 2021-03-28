from flask import url_for, request,jsonify

from server.app import db
from server.app.models import User
from server.app.api.errors import bad_request
from server.app.api import users_bp


@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return User.query.get_or_404(id).to_dict()


@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json or {}
    if 'username' not in data or 'email' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('users.get_user', id=user.id)
    return response
