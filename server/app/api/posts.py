from datetime import datetime
from typing import List

from flask import url_for, request, jsonify

from app import db
from app.models import Post, User
from app.api.errors import bad_request
from app.api import posts_bp


@posts_bp.route("/posts/<int:id>", methods=["GET"])
def get_post(id):
    return Post.query.get_or_404(id).to_dict()


@posts_bp.route('/posts', methods=['GET'])
def get_posts() -> List:
    """
    Get all the posts for a given user_id
    @return: list of posts
    """
    user_id = request.args.get("user_id")
    if user_id is None:
        return bad_request('must provide user_id')
    posts = Post.query.filter(User.id == user_id)
    response = []
    for post in posts:
        response.append(post.to_dict())
    response = jsonify(response)
    return response


@posts_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.json or {}
    if 'post' not in data or 'user_id' not in data:
        return bad_request('must include post and user_id fields')
    post = Post()
    post.from_dict(data)
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('posts.get_post', id=post.id)
    return response


@posts_bp.route('/posts/<int:id>', methods=['PATCH'])
def update_posts(id):
    post = Post.query.get_or_404(id)
    data = request.get_json() or {}
    data['last_modified'] = datetime.utcnow()
    post.from_dict(data)
    db.session.commit()
    return jsonify(post.to_dict())


@posts_bp.route('/posts/<int:id>', methods=['DELETE'])
def delete_posts(id):
    # TODO: instead of direct deletion, schedule deletion
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    return jsonify({})
