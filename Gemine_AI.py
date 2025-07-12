import google.generativeai as genai
import os

def get_api_key():
    """
    Get API key from Streamlit secrets if available,
    else from environment variables (for local fallback).
    """
    try:
        import streamlit as st
        return st.secrets["GEMINI_API_KEY"]
    except ImportError:
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv("GEMINI_API_KEY")
    except Exception as e:
        print(f"Error loading Streamlit secret: {e}")
        return None

# Configure Gemini API
api_key = get_api_key()
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-pro")
else:
    model = None
    print("❌ API key not found. Set GEMINI_API_KEY in Streamlit secrets or .env file.")

def chat_with_gemini():
    if not model:
        print("❌ Gemini model is not configured.")
        return

    print("🤖 Welcome to Gemini Chatbot! (type 'exit' to quit)\n")
    conversation_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("👋 Goodbye!")
            break

        conversation_history.append(f"User: {user_input}")
        prompt = "\n".join(conversation_history) + "\nAssistant:"

        try:
            response = model.generate_content(prompt)
            bot_reply = response.text.strip()
            print("Bot:", bot_reply)
            conversation_history.append(f"Assistant: {bot_reply}")
        except Exception as e:
            print(f"⚠️ Error generating response: {e}")
            print("Check your internet connection and Gemini API access.")

if __name__ == "__main__":
    if model:
        chat_with_gemini()
    else:
        print("""
🚨 ERROR: Gemini API Key not configured.

👉 If running on Streamlit Cloud:
   - Go to your app dashboard
   - Click ⋮ → Edit Secrets
   - Add this:
     GEMINI_API_KEY = "your-real-api-key"

👉 If running locally:
   - Install dotenv: pip install python-dotenv
   - Create a `.env` file:
     GEMINI_API_KEY=your-real-api-key
""")
