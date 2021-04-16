import os

from flask import current_app
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport import requests
from google.oauth2 import id_token

from server.journal import config


def create_credentials(token, refresh_token):
    credentials = {
        "token": token,
        "refresh_token": refresh_token,
        "token_uri": config.TOKEN_URI,
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "scopes": config.SCOPES,
    }
    return Credentials(**credentials)

    
def get_drive(token, refresh_token):
    credentials = create_credentials(token, refresh_token)
    return (build(config.API_SERVICE_NAME, 
        config.API_VERSION,
        credentials=credentials))


def get_client_config():
    return {
        "web": {
            "client_id": config.CLIENT_ID,
            "project_id": config.PROJECT_ID,
            "auth_uri": config.AUTH_URI,
            "token_uri": config.TOKEN_URI,
            "auth_provider_x509_cert_url": config.AUTH_PROVIDER_X509_CERT_URL,
            "client_secret": config.CLIENT_SECRET,
            "redirect_uris": config.REDIRECT_URIS
        }
    }

def validate_id_token(token):
    request = requests.Request()
    # TODO: hanlde token expiration
    id_info = id_token.verify_oauth2_token(token, request, config.CLIENT_ID)
    if id_info['iss'] != 'https://accounts.google.com':
        raise ValueError('Wrong issuer.')
    print(id_info)
    return id_info


def credentials_to_dict(credentials):
    return {
        "token": credentials["token"],
        "refresh_token": credentials["refresh_token"],
        "token_uri": credentials["token_uri"],
        "client_id": credentials["client_id"],
        "client_secret": credentials["client_secret"],
        "scopes": credentials["scopes"],
    }
