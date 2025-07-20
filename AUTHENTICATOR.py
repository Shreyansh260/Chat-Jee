import os
import json
import time
import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

def authenticate_user_manual():
    # ✅ If already authenticated, return immediately
    if "credentials" in st.session_state:
        return st.session_state["credentials"]
    
    # ✅ Load credentials JSON
    credentials_dict = json.loads(st.secrets["google_auth"]["credentials_json"])
    with open("temp_credentials.json", "w") as f:
        json.dump(credentials_dict, f)
    
    # ✅ Set up OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(
        "temp_credentials.json",
        SCOPES,
        redirect_uri="urn:ietf:wg:oauth:2.0:oob"
    )
    
    # ✅ Show auth UI container
    auth_container = st.container()
    
    with auth_container:
        # Step 1: Show auth link
        auth_url, _ = flow.authorization_url(prompt='consent')
        st.info("🔐 Please authenticate with Google:")
        st.markdown(f"[👉 Sign in with Google]({auth_url})", unsafe_allow_html=True)
        
        # Step 2: Wait for user input
        code = st.text_input("Paste the authorization code here:", key="auth_code")
        
        if code:
            try:
                # Step 3: Exchange code for credentials
                flow.fetch_token(code=code)
                creds = flow.credentials
                
                # Step 4: Get user info
                service = build('oauth2', 'v2', credentials=creds)
                user_info = service.userinfo().get().execute()
                
                # Step 5: Save to session
                st.session_state["credentials"] = {
                    "name": user_info.get("name"),
                    "email": user_info.get("email"),
                    "picture": user_info.get("picture")
                }
                
                # Step 6: Remove temp file
                if os.path.exists("temp_credentials.json"):
                    os.remove("temp_credentials.json")
                
                # ✅ CRITICAL: Clear the auth container and rerun
                auth_container.empty()
                st.success("✅ Authentication successful! Redirecting...")
                time.sleep(1)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Authentication failed: {e}")
                if os.path.exists("temp_credentials.json"):
                    os.remove("temp_credentials.json")
                return None
    
    return None
