import os

from flask import request, redirect, session, url_for, jsonify, current_app
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from . import auth_bp
from server.journal.models import User
from server.journal import config
from server.journal import db
from .utils.auth import get_client_config, validate_id_token, create_credentials

CLIENT_SECRETS_FILE = "/media/moz/max/projects/my-journal/server/journal/client_secret.json"
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


@auth_bp.route("/test")
def test_api_request():
    return "Welcome to journal"


@auth_bp.route("/authorize")
def authorize():
    # if not current_user.is_anonymous:
        # return redirect(url_for("auth.test_api_request"))

    # if current_user.is_authenticated:
    #     return redirect("localhost:3000/home")

    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = Flow.from_client_config(
        get_client_config(), scopes=config.SCOPES
    )

    # TODO: handle 'redirect_uri_mismatch' error
    flow.redirect_uri = url_for("auth.oauth2callback", _external=True)

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )

    # Store the state so the callback can verify the auth server response.
    print(state)
    session["state"] = state

    return redirect(authorization_url)


@auth_bp.route("/oauth2callback")
def oauth2callback():
    # if not current_user.is_anonymous:
        # return redirect(url_for("auth.test"))
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session["state"]

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=config.SCOPES, state=state
    )
    flow.redirect_uri = url_for("auth.oauth2callback", _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    # TODO: validate credentials, only then save in session otherwise redirect to auth
    
    id_info = validate_id_token(credentials.id_token)
    user = User.query.filter_by(google_id=id_info["sub"]).first()
    if not user:
        user = User(
            google_id=id_info["sub"],
            username=id_info["name"],
            email=id_info["email"],
            picture=id_info["picture"],
        )
        db.session.add(user)
        db.session.commit()
    login_user(user)
    print({"token": credentials.token, 
            "refresh_token": credentials.refresh_token, 
            "id_token": credentials.id_token})
    session["token"] = credentials.token
    session["refresh_token"] = credentials.refresh_token
    session["id_token"] = credentials.id_token

    return redirect(url_for("auth.test_api_request"))


@auth_bp.route("/refresh")
def refresh_tokens():
    if "refresh_token" not in session and "token" not in session:
        return (
            'You need to <a href="/authorize">authorize</a> before '
            + "testing the code to refresh credentials."
        )
    credentials = create_credentials(
        token=session["token"], refresh_token=session["refresh_token"]
    )
    # TODO: verify tokens
    if not credentials.valid and credentials.refresh_token:
        credentials.refresh(Request())
        session["token"] = credentials.token
        session["refresh_token"] = credentials.refresh_token
        session["id_token"] = credentials.id_token


@auth_bp.route("/revoke")
def revoke():
    if "refresh_token" not in session and "token" not in session:
        return (
            'You need to <a href="/authorize">authorize</a> before '
            + "testing the code to revoke credentials."
        )

    credentials = create_credentials(
        token=session["token"], refresh_token=session["refresh_token"]
    )

    revoke = requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    status_code = getattr(revoke, "status_code")
    if status_code == 200:
        return "Credentials successfully revoked."
    else:
        return "An error occurred."


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    if "refresh_token" in session or "token" in session or "id_token" in session:
        del session["refresh_token"]
        del session["token"]
        del session["id_token"]
    return redirect("https://localhost:3000")


# @auth_bp.route("/clear")
# def clear_credentials():
#     if "credentials" in session:
#         del session["credentials"]
#     return "Credentials have been cleared.<br><br>"
