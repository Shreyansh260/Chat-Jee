import os
import json
import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

def authenticate_user_manual():
    # Step 1: Load client secret from Streamlit secrets
    credentials_dict = json.loads(st.secrets["google_auth"]["credentials_json"])

    # Step 2: Save temporarily to file
    with open("temp_credentials.json", "w") as f:
        json.dump(credentials_dict, f)

    # Step 3: Start OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file("temp_credentials.json", SCOPES,redirect_uri='http://localhost')
    auth_url, _ = flow.authorization_url(prompt='consent')

    # Step 4: Prompt user to visit auth URL
    st.info("🔐 Please authenticate with Google:")
    st.markdown(f"[Click here to sign in with Google]({auth_url})", unsafe_allow_html=True)

    # Step 5: User pastes auth code manually
    code = st.text_input("Paste the authorization code here:")

    if code:
        try:
            flow.fetch_token(code=code)
            creds = flow.credentials

            # Get user info
            service = build('oauth2', 'v2', credentials=creds)
            user_info = service.userinfo().get().execute()

            return {
                "name": user_info.get("name"),
                "email": user_info.get("email"),
                "picture": user_info.get("picture"),
                "credentials": creds
            }

        except Exception as e:
            st.error(f"Authentication failed: {e}")
            return None
