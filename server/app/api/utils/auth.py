import os

from flask import current_app
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport import requests
from google.oauth2 import id_token


def create_credentials(token, refresh_token):
    credentials = {
        "token": token,
        "refresh_token": refresh_token,
        "token_uri": current_app.config.get("TOKEN_URI"),
        "client_id": current_app.config.get("CLIENT_ID"),
        "client_secret": current_app.config.get("CLIENT_SECRET"),
        "scopes": current_app.config.get("SCOPES"),
    }
    return Credentials(**credentials)

    
def get_drive(token, refresh_token):
    credentials = create_credentials(token, refresh_token)
    return (build(current_app.config['API_SERVICE_NAME'], 
        current_app.config.get("API_VERSION"),
        credentials=credentials))


def get_client_config():
    return {
        "web": {
            "client_id": os.environ.get("CLIENT_ID"),
            "project_id": os.environ.get("PROJECT_ID"),
            "auth_uri": os.environ.get("AUTH_URI"),
            "token_uri": os.environ.get("TOKEN_URI"),
            "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER_X509_CERT_URL"),
            "client_secret": os.environ.get("CLIENT_SECRET"),
            "redirect_uris": [os.environ.get("REDIRECT_URIS")]
        }
    }

def validate_id_token(token):
    request = requests.Request()
    id_info = id_token.verify_oauth2_token(token, request, os.environ.get("CLIENT_ID"))
    if id_info['iss'] != 'https://accounts.google.com':
        raise ValueError('Wrong issuer.')
    print(id_info)
    return id_info


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
