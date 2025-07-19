import os
import json
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

TOKEN_FILE = 'token.json'
USER_DB_FILE = 'users.json'

def save_user_info(user_info):
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'r') as f:
            users = json.load(f)
    else:
        users = []

    if not any(user['email'] == user_info['email'] for user in users):
        users.append(user_info)
        with open(USER_DB_FILE, 'w') as f:
            json.dump(users, f, indent=2)

def authenticate_user() -> dict:
    creds = None

    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception:
            os.remove(TOKEN_FILE)
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 🔐 Load credentials from Streamlit secrets
            credentials_dict = json.loads(st.secrets["google_auth"]["credentials_json"])

            # Save to a temporary JSON file
            with open("temp_credentials.json", "w") as f:
                json.dump(credentials_dict, f)

            flow = InstalledAppFlow.from_client_secrets_file("temp_credentials.json", SCOPES)
            creds = flow.run_local_server(port=0, open_browser=False)

            os.remove("temp_credentials.json")  # Clean up temp file

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    service = build('oauth2', 'v2', credentials=creds, cache_discovery=False)
    user_info = service.userinfo().get().execute()

    save_user_info({
        "name": user_info.get('name'),
        "email": user_info.get('email'),
        "picture": user_info.get('picture')
    })

    return user_info
