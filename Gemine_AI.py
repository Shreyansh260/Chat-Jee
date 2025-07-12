import google.generativeai as genai
import os

def get_api_key():
    """Get API key from Streamlit secrets only"""
    try:
        import streamlit as st
        return st.secrets["GEMINI_API_KEY"]
    except Exception as e:
        print(f"Error accessing Streamlit secrets: {e}")
        return None

# Configure with your Gemini API key
api_key = get_api_key()
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Warning: No API key found. Please set GEMINI_API_KEY in .env file or Streamlit secrets.")

# Select your model
model = genai.GenerativeModel("models/gemini-1.5-pro")

def chat_with_gemini():
    print("Welcome to Gemini Chatbot! (type 'exit' to quit)\n")
    conversation_history = []
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        
        # Prepare conversation context (optional, for simple context)
        conversation_history.append(f"User: {user_input}")
        prompt = "\n".join(conversation_history) + "\nAssistant:"
        
        try:
            # Generate response
            response = model.generate_content(prompt)
            bot_reply = response.text.strip()
            print("Bot:", bot_reply)
            
            # Save bot reply to history to keep context
            conversation_history.append(f"Assistant: {bot_reply}")
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please check your API key and internet connection.")

if __name__ == "__main__":
    # Check if API key is loaded
    if not get_api_key():
        print("Error: GEMINI_API_KEY not found in Streamlit secrets")
        print("Please set GEMINI_API_KEY in Streamlit secrets:")
        print("1. Go to your Streamlit app settings")
        print("2. Navigate to 'Secrets' section")
        print("3. Add: GEMINI_API_KEY = \"your_api_key_here\"")
    else:
        chat_with_gemini()
