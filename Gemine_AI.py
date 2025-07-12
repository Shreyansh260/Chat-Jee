import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure with your Gemini API key from .env file
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found in .env file")
        print("Please create a .env file with your API key")
    else:
        chat_with_gemini()
