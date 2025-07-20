import os
import json
import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

def authenticate_user_manual():
    # Load secrets from Streamlit
    credentials_dict = json.loads(st.secrets["google_auth"]["credentials_json"])

    # Save to temporary file
    with open("temp_credentials.json", "w") as f:
        json.dump(credentials_dict, f)

    # Initialize flow WITHOUT redirect_uri
    flow = InstalledAppFlow.from_client_secrets_file("temp_credentials.json", SCOPES)
    auth_url, _ = flow.authorization_url(prompt='consent')

    # Ask user to visit auth link
    st.info("🔐 Please authenticate with Google:")
    st.markdown(f"[👉 Sign in with Google]({auth_url})", unsafe_allow_html=True)

    # Manual input of code
    code = st.text_input("Paste the authorization code here:")

    if code:
        try:
            flow.fetch_token(code=code)
            creds = flow.credentials

            service = build('oauth2', 'v2', credentials=creds)
            user_info = service.userinfo().get().execute()

            # Clean up temp file
            if os.path.exists("temp_credentials.json"):
                os.remove("temp_credentials.json")

            return {
                "name": user_info.get("name"),
                "email": user_info.get("email"),
                "picture": user_info.get("picture"),
                "credentials": creds
            }

        except Exception as e:
            st.error(f"❌ Authentication failed: {e}")
            return None
