import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the .env file
load_dotenv()

# Access the Gemini API key from the environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Configure Gemini with the API key
genai.configure(api_key=api_key)

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
        
        # Prepare conversation context
        conversation_history.append(f"User: {user_input}")
        prompt = "\n".join(conversation_history) + "\nAssistant:"

        # Generate response
        response = model.generate_content(prompt)
        bot_reply = response.text.strip()

        print("Bot:", bot_reply)

        # Save bot reply to history
        conversation_history.append(f"Assistant: {bot_reply}")

if __name__ == "__main__":
    chat_with_gemini()
