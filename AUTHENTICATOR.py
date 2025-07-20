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
    # Already authenticated?
    if "credentials" in st.session_state:
        return st.session_state["credentials"]

    # Load credentials JSON from Streamlit secrets
    credentials_dict = json.loads(st.secrets["google_auth"]["credentials_json"])

    # Save to temp file
    with open("temp_credentials.json", "w") as f:
        json.dump(credentials_dict, f)

    # Setup OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(
        "temp_credentials.json",
        SCOPES,
        redirect_uri="urn:ietf:wg:oauth:2.0:oob"
    )

    # Step 1: Display Google Sign-in link
    auth_url, _ = flow.authorization_url(prompt='consent')
    st.info("🔐 Please authenticate with Google:")
    st.markdown(f"[👉 Sign in with Google]({auth_url})", unsafe_allow_html=True)

    # Step 2: Paste authorization code
    code = st.text_input("Paste the authorization code here:")

    # Step 3: If user provides code, exchange it
    if code:
        try:
            flow.fetch_token(code=code)
            creds = flow.credentials

            service = build('oauth2', 'v2', credentials=creds)
            user_info = service.userinfo().get().execute()

            # Store in session state
            st.session_state["credentials"] = {
                "name": user_info.get("name"),
                "email": user_info.get("email"),
                "picture": user_info.get("picture")
            }

            # Clean up temp file
            if os.path.exists("temp_credentials.json"):
                os.remove("temp_credentials.json")

            return st.session_state["credentials"]

        except Exception as e:
            st.error(f"❌ Authentication failed: {e}")
            return None

    return None
