import streamlit as st
from PyPDF2 import PdfReader
import hashlib
import time
import os
import re
from typing import Dict, List, Optional
from datetime import datetime
import logging

from AUTHENTICATOR import authenticate_user_manual

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import your Gemini AI module with better error handling
try:
    from Gemine_AI import model
    GEMINI_AVAILABLE = True
    logger.info("Gemini AI module loaded successfully")
except ImportError as e:
    logger.error(f"Failed to import Gemini AI: {e}")
    GEMINI_AVAILABLE = False
except Exception as e:
    logger.error(f"Unexpected error importing Gemini AI: {e}")
    GEMINI_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Chat Jee - JEE Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/Shreyansh260/chat-jee',
        'Report a bug': 'https://github.com/Shreyansh260/chat-jee/issues',
        'About': "# Chat Jee - Your AI JEE Preparation Assistant"
    }
)

# Enhanced CSS styling with animations and better responsiveness
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    
    
    /* Custom fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(16, 163, 127, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
        /* Hide main menu during authentication */
.stApp[data-auth="false"] #MainMenu {
    visibility: hidden !important;
}

/* Show loading state during auth transition */
.auth-loading {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 200px;
    font-size: 1.2rem;
    color: #10a37f;
}
    
    /* Chat container with glassmorphism effect */
    .chat-container {
        background: rgba(26, 26, 46, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 0;
        margin: 0;
        min-height: 60vh;
        max-height: 70vh;
        overflow-y: auto;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        scrollbar-width: thin;
        scrollbar-color: #444 transparent;
    }
    
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #10a37f, #667eea);
        border-radius: 4px;
    }
    
    .chat-container::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #0d8b63, #5a6fd8);
    }
    
    /* Enhanced message styling */
    .message {
        padding: 1.5rem;
        margin: 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        align-items: flex-start;
        gap: 16px;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .message:hover {
        background: rgba(255, 255, 255, 0.02);
    }
    
    .message-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
        margin-top: 4px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    
    .user-icon {
        background: linear-gradient(135deg, #10a37f, #0d8b63);
        color: white;
    }
    
    .bot-icon {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
    
    .message-content {
        flex-grow: 1;
        line-height: 1.7;
        font-size: 15px;
        word-wrap: break-word;
        color: #e0e0e0;
    }
    
    .user-message {
        background: rgba(45, 45, 72, 0.3);
    }
    
    .bot-message {
        background: rgba(26, 26, 46, 0.3);
    }
    
    /* Code blocks styling */
    .message-content pre {
        background: rgba(15, 15, 35, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 1rem;
        overflow-x: auto;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .message-content code {
        background: rgba(15, 15, 35, 0.6);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 13px;
    }
    
    /* Enhanced header with animated gradient */
    .header {
        text-align: center;
        padding: 3rem 1rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #10a37f 100%);
        background-size: 200% 200%;
        animation: gradientShift 6s ease infinite;
        border-radius: 0 0 24px 24px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .header h1 {
        color: white;
        margin: 0;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .header p {
        color: rgba(255, 255, 255, 0.9);
        margin: 0.5rem 0 0;
        font-size: 1.2rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* Enhanced input area */
    .stTextArea textarea {
        background: rgba(45, 45, 72, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 16px 60px 16px 20px !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
        resize: none !important;
        min-height: 60px !important;
        max-height: 200px !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #10a37f !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(16, 163, 127, 0.2) !important;
        background: rgba(45, 45, 72, 0.9) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, #10a37f, #0d8b63) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(16, 163, 127, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0d8b63, #10a37f) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(16, 163, 127, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Enhanced PDF upload area */
    .stFileUploader {
        background: rgba(45, 45, 72, 0.3) !important;
        border: 2px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .stFileUploader:hover {
        border-color: #10a37f !important;
        background: rgba(45, 45, 72, 0.5) !important;
    }
    
    .stFileUploader label {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* Status messages */
    .stSuccess {
        background: rgba(26, 46, 26, 0.8) !important;
        border: 1px solid rgba(16, 163, 127, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stError {
        background: rgba(46, 26, 26, 0.8) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stWarning {
        background: rgba(46, 39, 26, 0.8) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stInfo {
        background: rgba(26, 39, 46, 0.8) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Enhanced welcome message */
    .welcome-message {
        text-align: center;
        padding: 3rem 2rem;
        color: #ccc;
        position: relative;
    }
    
    .welcome-message h2 {
        color: #ffffff;
        margin-bottom: 1rem;
        font-size: 2rem;
        font-weight: 600;
    }
    
    .welcome-message p {
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    /* Enhanced sample questions */
    .sample-questions {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .sample-question {
        background: rgba(45, 45, 72, 0.4);
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: left;
        position: relative;
        overflow: hidden;
    }
    
    .sample-question::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(16, 163, 127, 0.1), rgba(102, 126, 234, 0.1));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .sample-question:hover::before {
        opacity: 1;
    }
    
    .sample-question:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        border-color: rgba(16, 163, 127, 0.3);
    }
    
    .sample-question strong {
        color: #10a37f;
        font-weight: 600;
        position: relative;
        z-index: 1;
    }
    
    .sample-question span {
        position: relative;
        z-index: 1;
    }
    
    /* Enhanced typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 1rem;
        color: #10a37f;
        font-style: italic;
        font-weight: 500;
    }
    
    .typing-dots {
        display: flex;
        gap: 6px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: linear-gradient(135deg, #10a37f, #0d8b63);
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dot:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.4;
        }
        30% {
            transform: translateY(-8px);
            opacity: 1;
        }
    }
    
    /* Enhanced expander */
    .streamlit-expanderHeader {
        background: rgba(45, 45, 72, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(26, 26, 46, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 0 0 12px 12px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Statistics card */
    .stats-card {
        background: rgba(45, 45, 72, 0.4);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .stats-card h3 {
        color: #10a37f;
        margin: 0 0 0.5rem 0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .stats-card p {
        color: #ccc;
        margin: 0;
        font-size: 0.9rem;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .header h1 {
            font-size: 2.5rem;
        }
        
        .header p {
            font-size: 1rem;
        }
        
        .sample-questions {
            grid-template-columns: 1fr;
        }
        
        .message {
            padding: 1rem;
        }
        
        .welcome-message {
            padding: 2rem 1rem;
        }
        
        .welcome-message h2 {
            font-size: 1.5rem;
        }
    }
    
    /* Pulse animation for loading */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
</style>
""", unsafe_allow_html=True)

class EnhancedChatJee:
    def __init__(self):
        self.conversation_history = []
        self.pdf_content = ""
        self.session_start_time = datetime.now()
        self.total_messages = 0
        self.pdf_files_processed = 0
        
    def validate_pdf_file(self, pdf_file) -> bool:
        """Validate PDF file before processing"""
        try:
            if pdf_file.size > 10 * 1024 * 1024:  # 10MB limit
                st.error("❌ File size too large. Please upload files smaller than 10MB.")
                return False
            
            if not pdf_file.name.lower().endswith('.pdf'):
                st.error("❌ Invalid file format. Please upload only PDF files.")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error validating PDF: {e}")
            return False
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file with better error handling"""
        try:
            if not self.validate_pdf_file(pdf_file):
                return ""
            
            pdf_reader = PdfReader(pdf_file)
            text = ""
            
            if len(pdf_reader.pages) == 0:
                st.warning("⚠️ PDF appears to be empty or corrupted.")
                return ""
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():
                        text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                except Exception as e:
                    logger.warning(f"Error extracting text from page {page_num + 1}: {e}")
                    continue
            
            if not text.strip():
                st.warning("⚠️ No text could be extracted from the PDF. It might be image-based.")
                return ""
            
            return text
        except Exception as e:
            logger.error(f"Error reading PDF {pdf_file.name}: {e}")
            st.error(f"❌ Error reading PDF: {str(e)}")
            return ""
    
    def process_pdfs(self, uploaded_files) -> str:
        """Process multiple PDF files with progress tracking"""
        all_text = ""
        successful_files = 0
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, file in enumerate(uploaded_files):
            progress = (i + 1) / len(uploaded_files)
            progress_bar.progress(progress)
            status_text.text(f"Processing {file.name}... ({i + 1}/{len(uploaded_files)})")
            
            text = self.extract_text_from_pdf(file)
            if text:
                all_text += f"\n\n{'='*50}\n📄 Content from {file.name}\n{'='*50}\n{text}"
                successful_files += 1
        
        progress_bar.empty()
        status_text.empty()
        
        if successful_files > 0:
            self.pdf_files_processed = successful_files
            st.success(f"✅ Successfully processed {successful_files} out of {len(uploaded_files)} PDF(s)")
        else:
            st.error("❌ No PDFs could be processed successfully.")
        
        return all_text
    
    def clean_and_format_response(self, response: str) -> str:
        """Clean and format the AI response"""
        # Remove excessive newlines
        response = re.sub(r'\n{3,}', '\n\n', response)
        
        # Format mathematical expressions
        response = re.sub(r'\*\*(.*?)\*\*', r'**\1**', response)
        
        # Format code blocks
        response = re.sub(r'```(\w+)?\n(.*?)```', r'```\1\n\2\n```', response, flags=re.DOTALL)
        
        return response.strip()
    
    def get_response(self, user_input: str) -> str:
        """Get AI response with enhanced error handling"""
        try:
            if not GEMINI_AVAILABLE:
                return """❌ **Gemini AI module not available**
                
Please ensure that:
1. The `Gemine_AI.py` file is in the same directory
2. The Gemini API is properly configured
3. You have a valid API key

You can still use this interface once you fix the AI module."""
            
            # Input validation
            if not user_input.strip():
                return "Please enter a question or message."
            
            if len(user_input) > 5000:
                return "⚠️ Your message is too long. Please keep it under 5000 characters."
            
            # Create enhanced context
            context = f"""You are Chat Jee, an expert AI tutor specialized in JEE (Joint Entrance Examination) preparation.

{"📚 **Available Study Materials:**" + self.pdf_content[:10000] + "..." if self.pdf_content else ""}

**Previous Conversation Context:**
{chr(10).join(self.conversation_history[-8:])}

**Current Student Question:** {user_input}

**Instructions:**
- Provide clear, detailed, and step-by-step explanations
- Use proper formatting with headings, bullet points, and code blocks where appropriate
- Include relevant examples and practice problems
- Be encouraging and supportive
- If solving numerical problems, show all steps clearly
- For conceptual questions, provide intuitive explanations
- Reference JEE syllabus and previous year questions when relevant

**Response Format:**
- Use markdown formatting for better readability
- Include emojis to make responses more engaging
- Structure your response with clear sections
- Provide additional resources or practice suggestions when helpful
"""
            
            # Get response from AI
            response = model.generate_content(context)
            bot_reply = response.text.strip()
            
            # Clean and format response
            bot_reply = self.clean_and_format_response(bot_reply)
            
            # Update conversation history
            self.conversation_history.append(f"Student: {user_input}")
            self.conversation_history.append(f"Chat Jee: {bot_reply}")
            
            # Keep only last 20 exchanges to manage memory
            if len(self.conversation_history) > 40:
                self.conversation_history = self.conversation_history[-40:]
            
            self.total_messages += 1
            
            return bot_reply
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"""❌ **Error generating response**
            
I encountered an error while processing your question: `{str(e)}`

**Possible solutions:**
1. Try rephrasing your question
2. Check your internet connection
3. Ensure the AI module is properly configured
4. Contact support if the issue persists

Please try again with a different question."""
    
    def get_session_stats(self) -> Dict:
        """Get session statistics"""
        session_duration = datetime.now() - self.session_start_time
        return {
            "duration": str(session_duration).split('.')[0],
            "messages": self.total_messages,
            "pdfs_processed": self.pdf_files_processed,
            "has_materials": bool(self.pdf_content)
        }

def create_sample_questions():
    """Create sample questions with better formatting"""
    sample_questions = [
        {
            "category": "📐 Mathematics",
            "icon": "📐",
            "question": "Explain the concept of limits in calculus with step-by-step examples",
            "color": "#10a37f"
        },
        {
            "category": "⚡ Physics", 
            "icon": "⚡",
            "question": "Solve a rotational motion problem with detailed solution steps",
            "color": "#667eea"
        },
        {
            "category": "🧪 Chemistry",
            "icon": "🧪", 
            "question": "Important organic chemistry reactions and mechanisms for JEE",
            "color": "#764ba2"
        },
        {
            "category": "📝 Previous Years",
            "icon": "📝",
            "question": "JEE Main 2023 coordinate geometry previous year questions",
            "color": "#f59e0b"
        },
        {
            "category": "🎯 Problem Solving",
            "icon": "🎯",
            "question": "Time management strategies for JEE Main examination",
            "color": "#ef4444"
        },
        {
            "category": "📊 Revision",
            "icon": "📊",
            "question": "Quick revision notes for thermodynamics concepts",
            "color": "#8b5cf6"
        }
    ]
    
    questions_html = "<div class='sample-questions'>"
    for q in sample_questions:
        questions_html += f"""
        <div class="sample-question" onclick="document.getElementById('chat_input').value='{q['question']}'">
            <strong style="color: {q['color']};">{q['icon']} {q['category']}</strong><br>
            <span>"{q['question']}"</span>
        </div>
        """
    questions_html += "</div>"
    
    return questions_html

def main():
    def initialize_session_state():
        """Initialize all session state variables"""
        if 'chatbot' not in st.session_state:
            st.session_state.chatbot = EnhancedChatJee()
    
        if 'messages' not in st.session_state:
            st.session_state.messages = []
    
        if 'pdf_uploaded' not in st.session_state:
            st.session_state.pdf_uploaded = False
    
        if 'processing' not in st.session_state:
            st.session_state.processing = False
    
        if 'authentication_complete' not in st.session_state:
            st.session_state.authentication_complete = False
    initialize_session_state()
    
    # Handle authentication
    user_info = authenticate_user_manual()
    
    if not user_info:
        # Authentication UI is already shown in authenticate_user_manual()
        # Just stop execution here
        st.stop()
    
    # Mark authentication as complete
    st.session_state.authentication_complete = True
    
    # Show user info in sidebar (clean version)
    with st.sidebar:
        st.success(f"👋 Hello, {user_info['name']}!")
        if user_info.get('picture'):
            st.image(user_info['picture'], width=80)
        st.write(f"📧 {user_info['email']}")
        st.markdown("---")

        
        # Add logout button
        logout_col1, logout_col2 = st.columns([1, 1])
        
        with logout_col1:
            if st.button("🚪 Logout", key="main_logout", type="secondary", use_container_width=True):
                # Method 1: Use the imported logout function
                from AUTHENTICATOR import logout_user
                logout_user()
                
    # Header with enhanced styling
    st.markdown("""
        <div class="header">
        <h1>🎓 Chat Jee</h1>
        <p>Your AI-powered JEE preparation assistant with personalized learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar with session stats
    with st.sidebar:
        st.markdown("### 📊 Session Statistics")
        stats = st.session_state.chatbot.get_session_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Messages", stats["messages"])
            st.metric("PDFs Processed", stats["pdfs_processed"])
        with col2:
            st.metric("Session Time", stats["duration"])
            st.metric("Materials", "Yes" if stats["has_materials"] else "No")
        
        st.markdown("---")
        st.markdown("### 🔧 Quick Actions")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            st.session_state.chatbot.conversation_history = []
            st.success("Chat history cleared!")
            st.rerun()
        
        if st.button("📄 Clear PDF Materials"):
            st.session_state.chatbot.pdf_content = ""
            st.session_state.pdf_uploaded = False
            st.success("PDF materials cleared!")
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ About Chat Jee")
        st.markdown("""
        Chat Jee is an AI-powered assistant designed specifically for JEE preparation. 
        It can help you with:
        - Concept explanations
        - Problem solving
        - Previous year questions
        - Study strategies
        - Doubt resolution
        """)
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # PDF Upload section
        with st.expander("📚 Upload Study Materials (Optional)", expanded=not st.session_state.pdf_uploaded):
            if not GEMINI_AVAILABLE:
                st.error("⚠️ AI module not available. Please fix the Gemini AI configuration first.")
            else:
                uploaded_files = st.file_uploader(
                    "Upload your JEE study materials (PDF files)",
                    type=['pdf'],
                    accept_multiple_files=True,
                    help="Upload multiple PDF files to enhance the AI's knowledge base for personalized assistance."
                )
                
                if uploaded_files:
                    st.info(f"📄 {len(uploaded_files)} file(s) selected")
                    
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        if st.button("🚀 Process PDFs", type="primary", use_container_width=True):
                            with st.spinner("🔄 Processing your study materials..."):
                                try:
                                    pdf_content = st.session_state.chatbot.process_pdfs(uploaded_files)
                                    if pdf_content:
                                        st.session_state.chatbot.pdf_content = pdf_content
                                        st.session_state.pdf_uploaded = True
                                        time.sleep(1)
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"❌ Error processing PDFs: {str(e)}")
                    
                    with col_b:
                        if st.button("🗑️ Clear", use_container_width=True):
                            st.session_state.chatbot.pdf_content = ""
                            st.session_state.pdf_uploaded = False
                            st.rerun()
                
                if st.session_state.pdf_uploaded:
                    st.success("✅ Study materials loaded successfully!")
                    st.info("💡 You can now ask questions about your uploaded materials.")
        
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Welcome message or chat history
            if not st.session_state.messages:
                st.markdown(f"""
                <div class="welcome-message">
                    <h2>👋 Welcome to Chat Jee!</h2>
                    <p>I'm your AI-powered JEE preparation assistant. I can help you with:</p>
                    <p><strong>Mathematics • Physics • Chemistry • Problem Solving • Concepts • Previous Year Questions</strong></p>
                    <p>💡 <em>Try clicking on any sample question below to get started!</em></p>
                </div>
                <div class="sample-questions">
                    {create_sample_questions()}
                </div>
                """, unsafe_allow_html=True)
            
            # Display messages
            for i, message in enumerate(st.session_state.messages):
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="message user-message">
                        <div class="message-icon user-icon">👤</div>
                        <div class="message-content">{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="message bot-message">
                        <div class="message-icon bot-icon">🎓</div>
                        <div class="message-content">{message["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show typing indicator when processing
            if st.session_state.processing:
                st.markdown("""
                <div class="message bot-message">
                    <div class="message-icon bot-icon">🎓</div>
                    <div class="typing-indicator">
                        Chat Jee is thinking
                        <div class="typing-dots">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Input area with enhanced styling
       # Replace the entire input section and shortcut buttons section with this corrected version:

        # Input area with enhanced styling
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Input form
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Message Chat Jee...",
                placeholder="Ask me anything about JEE preparation... (e.g., 'Explain integration by parts' or 'Solve a thermodynamics problem')",
                height=80,
                max_chars=5000,
                key="user_input",
                label_visibility="collapsed",
                help="Type your question here and press Ctrl+Enter to send"
            )
            
            # Form buttons
            col_1, col_2, col_3 = st.columns([1, 2, 1])
            with col_2:
                submitted = st.form_submit_button(
                    "🚀 Send Message", 
                    type="primary", 
                    use_container_width=True,
                    disabled=st.session_state.processing
                )

        # Handle form submission OUTSIDE the form context
        if submitted and user_input.strip():
            if not GEMINI_AVAILABLE:
                st.error("❌ Cannot send message. Please fix the Gemini AI configuration first.")
            else:
                # Add user message
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Show processing state and rerun to display it
                st.session_state.processing = True
                st.rerun()
        
        # Handle response generation when processing is True
        if st.session_state.processing:
            try:
                # Get the last user message
                last_user_message = None
                for msg in reversed(st.session_state.messages):
                    if msg["role"] == "user":
                        last_user_message = msg["content"]
                        break
                
                if last_user_message:
                    # Get AI response
                    response = st.session_state.chatbot.get_response(last_user_message)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Clear processing state
                st.session_state.processing = False
                st.rerun()
                
            except Exception as e:
                error_msg = f"""❌ **Error generating response**
                
I encountered an unexpected error: `{str(e)}`

**Please try:**
1. Refreshing the page
2. Rephrasing your question
3. Checking your internet connection
4. Contacting support if the issue persists"""
                
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                logger.error(f"Error in response generation: {e}")
                
                # Clear processing state
                st.session_state.processing = False
                st.rerun()
    
    # MOVE THE COLUMN LAYOUT OUTSIDE THE FORM CONTEXT
    with col2:
        # Quick tips panel
        st.markdown("### 💡 Quick Tips")
        tips = [
            "📝 Be specific in your questions",
            "🔢 Include numbers for calculations", 
            "📚 Upload PDFs for personalized help",
            "🎯 Ask for step-by-step solutions",
            "📊 Request practice problems",
            "⏰ Ask about time management"
        ]
        
        for tip in tips:
            st.markdown(f"• {tip}")
        
        st.markdown("---")
        
        # Subject shortcuts - NOW OUTSIDE THE FORM
        st.markdown("### 🎯 Subject Shortcuts")
        
        shortcuts = [
            ("📐 Math", "Explain calculus concepts"),
            ("⚡ Physics", "Solve mechanics problems"),
            ("🧪 Chemistry", "Organic reactions"),
            ("📝 Previous Years", "JEE Main 2023 questions"),
            ("🎓 Study Tips", "Effective preparation strategies")
        ]
        
        for label, query in shortcuts:
            if st.button(label, key=f"shortcut_{label}", use_container_width=True):
                if not GEMINI_AVAILABLE:
                    st.error("❌ AI module not available")
                else:
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": query})
                    
                    # Show processing state
                    st.session_state.processing = True
                    st.rerun()
        
        st.markdown("---")
        
        # Status indicator
        if GEMINI_AVAILABLE:
            st.success("✅ AI Ready")
        else:
            st.error("❌ AI Unavailable")
            
        if st.session_state.chatbot.pdf_content:
            st.info("📚 Materials Loaded")
        else:
            st.warning("📄 No Materials")
    
    # Footer with additional information
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #888;">
        <p>🎓 <strong>Chat Jee</strong> - Your AI JEE Preparation Assistant</p>
        <p>Built with ❤️ for JEE aspirants | Enhanced with modern UI and robust error handling</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-scroll JavaScript
    st.markdown("""
    <script>
        // Auto-scroll to bottom function
        function scrollToBottom() {
            window.scrollTo({
                top: document.body.scrollHeight,
                behavior: 'smooth'
            });
        }
        
        // Scroll to bottom when new messages appear
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    // Check if new message was added
                    const newNodes = Array.from(mutation.addedNodes);
                    if (newNodes.some(node => node.classList && node.classList.contains('message'))) {
                        setTimeout(scrollToBottom, 100);
                    }
                }
            });
        });
        
        // Start observing
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        // Handle keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // Ctrl+Enter to send message
            if (e.ctrlKey && e.key === 'Enter') {
                const sendButton = document.querySelector('button[kind="primary"]');
                if (sendButton && !sendButton.disabled) {
                    sendButton.click();
                }
            }
            
            // Escape to clear input
            if (e.key === 'Escape') {
                const textarea = document.querySelector('textarea');
                if (textarea) {
                    textarea.value = '';
                    textarea.focus();
                }
            }
        });
        
        // Focus on input when page loads
        window.addEventListener('load', function() {
            const textarea = document.querySelector('textarea');
            if (textarea) {
                textarea.focus();
            }
        });
    </script>
    """, unsafe_allow_html=True)
    

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Critical error in main(): {e}")
        st.error(f"""
        🚨 **Critical Error**
        
        The application encountered a critical error: `{str(e)}`
        
        **Please try:**
        1. Refreshing the page
        2. Restarting the Streamlit application
        3. Checking your Python environment
        4. Ensuring all dependencies are installed
        
        If the problem persists, please contact support.
        """)
        
        # Show error details in expander for debugging
        with st.expander("🔍 Technical Details (for developers)"):
            st.exception(e)
