from datetime import datetime
from typing import List
import json
from io import BytesIO

from flask import url_for, request, jsonify, session

from server.app import db
from server.app.models import Post, User
from server.app.api.errors import bad_request
from server.app.api import posts_bp
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload


@posts_bp.route("/posts/<int:id>", methods=["GET"])
def get_post(id):
    post_data = Post.query.get_or_404(id).to_dict()
    drive_service = build("drive", "v3", credentials=session.get("credentials"))
    request = drive_service.files().get_media(fileId=post_data["post_file_id"])
    text_stream = BytesIO()
    downloader = MediaIoBaseDownload(text_stream, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    if done == True:
        post_data["post_text"] = text_stream.getvalue().decode("utf-8")
    return post_data


@posts_bp.route("/posts", methods=["GET"])
def get_posts() -> List:
    """
    Get all the posts for a given user_id
    @return: list of posts
    """
    user_id = request.args.get("user_id")
    if user_id is None:
        return bad_request("must provide user_id")
    posts = Post.query.filter(User.id == user_id)
    response = []
    drive_service = build("drive", "v3", credentials=session.get("credentials"))

    for post in posts:
        post_data = post.to_dict()
        request = drive_service.files().get_media(fileId=post_data["post_file_id"])
        text_stream = BytesIO()
        downloader = MediaIoBaseDownload(text_stream, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        if done == True:
            post_data["post_text"] = text_stream.getvalue().decode("utf-8")
            response.append(post_data)
    response = jsonify(response)
    return response


@posts_bp.route("/posts", methods=["POST"])
def create_post():
    data = request.json or {}
    if "post" not in data or "user_id" not in data:
        return bad_request("must include post and user_id fields")
    drive_service = build("drive", "v3", credentials=session.get("credentials"))
    filename: str = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S") + ".bin"
    post_bytes = BytesIO(data["post"].encode("utf-8"))
    file_metadata = {"name": filename, "parents": ["appDataFolder"]}
    # TODO: handle errors failure to upload
    media = MediaIoBaseUpload(post_bytes, mimetype="application/octet-stream")

    file = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )

    _ = data.pop("post")
    data["post_gdrive_name"] = filename
    data["post_gdrive_id"] = file["id"]
    post = Post()
    post.from_dict(data)
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("posts.get_post", id=post.id)
    return response


@posts_bp.route("/posts/<int:id>", methods=["PATCH"])
def update_posts(id):
    post = Post.query.get_or_404(id)
    data = request.get_json() or {}
    data["last_modified"] = datetime.utcnow()
    post.from_dict(data)
    db.session.commit()
    return jsonify(post.to_dict())


@posts_bp.route("/posts/<int:id>", methods=["DELETE"])
def delete_posts(id):
    # TODO: instead of direct deletion, schedule deletion
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    return jsonify({})
