import os
import json
import time
import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

def authenticate_user_manual():
    # ✅ Already logged in with token
    if "credentials" in st.session_state:
        return st.session_state["credentials"]
    
    # ✅ Try loading saved token from file
    if os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            
            # Check if token needs refresh
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    # Save refreshed token
                    with open("token.json", "w") as token_file:
                        token_file.write(creds.to_json())
                except Exception as e:
                    st.warning("⚠️ Token refresh failed, please login again.")
                    os.remove("token.json")
                    return None
            
            if creds and creds.valid:
                try:
                    service = build('oauth2', 'v2', credentials=creds)
                    user_info = service.userinfo().get().execute()
                    st.session_state["credentials"] = {
                        "name": user_info.get("name"),
                        "email": user_info.get("email"),
                        "picture": user_info.get("picture"),
                        "token": creds.token
                    }
                    return st.session_state["credentials"]
                except Exception as e:
                    st.warning("⚠️ Token expired or invalid, please login again.")
                    os.remove("token.json")
            else:
                # Token invalid, remove file
                os.remove("token.json")
        except Exception as e:
            st.warning(f"⚠️ Error loading token: {e}")
            if os.path.exists("token.json"):
                os.remove("token.json")
    
    # ✅ OAuth flow - only if not already authenticated
    try:
        credentials_dict = json.loads(st.secrets["google_auth"]["credentials_json"])
    except KeyError:
        st.error("❌ Google OAuth credentials not found in secrets.")
        return None
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON in Google OAuth credentials.")
        return None
    
    # Create temp credentials file
    with open("temp_credentials.json", "w") as f:
        json.dump(credentials_dict, f)
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            "temp_credentials.json",
            SCOPES,
            redirect_uri="urn:ietf:wg:oauth:2.0:oob"
        )
        
        # 🔐 Login UI container to prevent duplication
        auth_container = st.container()
        
        with auth_container:
            # FIXED: Correct method call
            auth_url, _ = flow.authorization_url(prompt='consent')
            st.info("🔐 Please authenticate with Google:")
            st.markdown(f"[👉 Sign in with Google]({auth_url})")
            
            code = st.text_input("Paste the authorization code here:", key="auth_code")
            
            if code:
                try:
                    flow.fetch_token(code=code)
                    creds = flow.credentials
                    
                    # Save token to file for future use
                    with open("token.json", "w") as token_file:
                        token_file.write(creds.to_json())
                    
                    # Get user info
                    service = build('oauth2', 'v2', credentials=creds)
                    user_info = service.userinfo().get().execute()
                    
                    # Save in session
                    st.session_state["credentials"] = {
                        "name": user_info.get("name"),
                        "email": user_info.get("email"),
                        "picture": user_info.get("picture"),
                        "token": creds.token
                    }
                    
                    # Clean up temp file
                    if os.path.exists("temp_credentials.json"):
                        os.remove("temp_credentials.json")
                    
                    # Clear the auth container and rerun
                    auth_container.empty()
                    st.success("✅ Login successful! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Authentication failed: {e}")
                    # Clean up on error
                    if os.path.exists("temp_credentials.json"):
                        os.remove("temp_credentials.json")
                    return None
    
    except Exception as e:
        st.error(f"❌ OAuth setup failed: {e}")
        if os.path.exists("temp_credentials.json"):
            os.remove("temp_credentials.json")
        return None
    
    return None

def logout_user():
    """Fixed logout function with proper session state clearing"""
    try:
        # Remove from session state - clear ALL keys to ensure clean logout
        keys_to_remove = list(st.session_state.keys())
        for key in keys_to_remove:
            del st.session_state[key]
        
        # Remove token file
        if os.path.exists("token.json"):
            os.remove("token.json")
            
        # Remove temp credentials if exists
        if os.path.exists("temp_credentials.json"):
            os.remove("temp_credentials.json")
        
        st.success("✅ Logged out successfully! Redirecting...")
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Logout failed: {e}")
        # Force clear session state even if file operations fail
        try:
            keys_to_remove = list(st.session_state.keys())
            for key in keys_to_remove:
                del st.session_state[key]
            st.rerun()
        except:
            st.error("Please refresh the page manually to complete logout.")

# Alternative logout function with more aggressive clearing
def force_logout():
    """Alternative logout function with more aggressive clearing"""
    try:
        # Clear session state
        st.session_state.clear()
        
        # Remove files
        files_to_remove = ["token.json", "temp_credentials.json"]
        for file in files_to_remove:
            try:
                if os.path.exists(file):
                    os.remove(file)
            except Exception as e:
                st.warning(f"Could not remove {file}: {e}")
        
        # Show success and refresh
        st.success("✅ Logout successful!")
        st.balloons()  # Visual feedback
        time.sleep(2)
        
        # Use JavaScript to force refresh the page
        st.markdown("""
        <script>
        setTimeout(function() {
            window.location.reload();
        }, 2000);
        </script>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ Logout error: {e}")
        st.info("Please refresh the page manually to complete logout.")

# Example usage
def main():
    st.title("🔐 Google Authentication Demo")
    
    # Add logout button in sidebar if user is authenticated
    if "credentials" in st.session_state:
        with st.sidebar:
            user = st.session_state["credentials"]
            st.write(f"👋 Welcome, **{user['name']}**")
            
            # Create two columns for logout buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚪 Logout", key="logout_normal"):
                    logout_user()
            with col2:
                if st.button("🔄 Force Logout", key="logout_force"):
                    force_logout()
    
    # Try to authenticate
    user = authenticate_user_manual()
    
    if user:
        st.success("🎉 You are successfully logged in!")
        st.json(user)
    else:
        st.info("Please authenticate to continue")

if __name__ == "__main__":
    main()
