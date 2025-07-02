import streamlit as st
from PyPDF2 import PdfReader
import io
import time
from typing import List, Dict
import hashlib

# Import your Gemini AI module
try:
    from Gemine_AI import model
    GEMINI_AVAILABLE = True
except ImportError:
    st.error("❌ Gemine_AI.py file not found! Please ensure it's in the same directory.")
    GEMINI_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Chat Jee - JEE Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fixed Custom CSS for better UI visibility
st.markdown("""
<style>
    /* CSS Variables for theme adaptation */
    :root {
        /* Light theme colors */
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-tertiary: #f5f5f5;
        --text-primary: #1f2937;
        --text-secondary: #4b5563;
        --text-tertiary: #6b7280;
        --border-color: #e5e7eb;
        --border-hover: #d1d5db;
        --shadow: rgba(0, 0, 0, 0.1);
        --shadow-hover: rgba(0, 0, 0, 0.15);

        /* Chat message colors - light theme */
        --user-bg: #dbeafe;
        --user-border: #3b82f6;
        --user-text: #1e40af;
        --user-text-strong: #1d4ed8;

        --bot-bg: #f3e8ff;
        --bot-border: #a855f7;
        --bot-text: #7c2d92;
        --bot-text-strong: #86198f;

        /* Status colors - light theme */
        --success-bg: #dcfce7;
        --success-border: #22c55e;
        --success-text: #166534;
        --success-text-strong: #15803d;

        --error-bg: #fef2f2;
        --error-border: #ef4444;
        --error-text: #dc2626;
        --error-text-strong: #b91c1c;

        --warning-bg: #fef3c7;
        --warning-border: #f59e0b;
        --warning-text: #d97706;
        --warning-text-strong: #b45309;

        --info-bg: #dbeafe;
        --info-border: #3b82f6;
        --info-text: #1d4ed8;
        --info-text-strong: #1e40af;

        /* Form colors - light theme */
        --input-bg: #ffffff;
        --input-border: #d1d5db;
        --input-border-focus: #3b82f6;
        --input-text: #1f2937;
    }

    /* Dark theme colors */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #23263a;
            --bg-secondary: #181a28;
            --bg-tertiary: #23263a;
            --text-primary: #f5f6fa;
            --text-secondary: #cdd6f4;
            --text-tertiary: #bac2de;
            --border-color: #313244;
            --border-hover: #45475a;
            --shadow: rgba(0, 0, 0, 0.7);
            --shadow-hover: rgba(0, 0, 0, 0.85);

            /* Chat message colors - dark theme */
            --user-bg: #274690;
            --user-border: #89b4fa;
            --user-text: #e0e7ff;
            --user-text-strong: #b4befe;

            --bot-bg: #5f2a8e;
            --bot-border: #cba6f7;
            --bot-text: #f5c2e7;
            --bot-text-strong: #f2cdcd;

            /* Status colors - dark theme */
            --success-bg: #1e5128;
            --success-border: #94e2d5;
            --success-text: #a6e3a1;
            --success-text-strong: #94e2d5;

            --error-bg: #7c1d1d;
            --error-border: #eba0ac;
            --error-text: #f38ba8;
            --error-text-strong: #eba0ac;

            --warning-bg: #b45309;
            --warning-border: #f9e2af;
            --warning-text: #fab387;
            --warning-text-strong: #f9e2af;

            --info-bg: #274690;
            --info-border: #89b4fa;
            --info-text: #e0e7ff;
            --info-text-strong: #b4befe;

            /* Form colors - dark theme */
            --input-bg: #23263a;
            --input-border: #313244;
            --input-border-focus: #89b4fa;
            --input-text: #f5f6fa;
        }
    }

    /* Manual dark theme class override */
    .dark-theme {
        --bg-primary: #23263a;
        --bg-secondary: #181a28;
        --bg-tertiary: #23263a;
        --text-primary: #f5f6fa;
        --text-secondary: #cdd6f4;
        --text-tertiary: #bac2de;
        --border-color: #313244;
        --border-hover: #45475a;
        --shadow: rgba(0, 0, 0, 0.7);
        --shadow-hover: rgba(0, 0, 0, 0.85);

        --user-bg: #274690;
        --user-border: #89b4fa;
        --user-text: #e0e7ff;
        --user-text-strong: #b4befe;

        --bot-bg: #5f2a8e;
        --bot-border: #cba6f7;
        --bot-text: #f5c2e7;
        --bot-text-strong: #f2cdcd;

        --success-bg: #1e5128;
        --success-border: #94e2d5;
        --success-text: #a6e3a1;
        --success-text-strong: #94e2d5;

        --error-bg: #7c1d1d;
        --error-border: #eba0ac;
        --error-text: #f38ba8;
        --error-text-strong: #eba0ac;

        --warning-bg: #b45309;
        --warning-border: #f9e2af;
        --warning-text: #fab387;
        --warning-text-strong: #f9e2af;

        --info-bg: #274690;
        --info-border: #89b4fa;
        --info-text: #e0e7ff;
        --info-text-strong: #b4befe;

        --input-bg: #23263a;
        --input-border: #313244;
        --input-border-focus: #89b4fa;
        --input-text: #f5f6fa;
    }

    
    /* Main app styling */
    .stApp {
        background-color: var(--bg-secondary);
        color: var(--text-primary);
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    
    .main-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px var(--shadow);
        transition: box-shadow 0.3s ease;
    }
    
    .main-header h1 {
        color: white !important;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #f0f0f0 !important;
        margin-bottom: 0.3rem;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px var(--shadow);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .user-message {
        background-color: var(--user-bg);
        border-left: 4px solid var(--user-border);
        color: var(--user-text);
    }
    
    .user-message strong {
        color: var(--user-text-strong) !important;
    }
    
    .bot-message {
        background-color: var(--bot-bg);
        border-left: 4px solid var(--bot-border);
        color: var(--bot-text);
    }
    
    .bot-message strong {
        color: var(--bot-text-strong) !important;
    }
    
    /* PDF info styling */
    .pdf-info {
        background-color: var(--warning-bg);
        color: var(--warning-text);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid var(--warning-border);
        margin: 1rem 0;
        border: 1px solid var(--warning-border);
        transition: all 0.3s ease;
    }
    
    .pdf-info strong {
        color: var(--warning-text-strong) !important;
    }
    
    /* Status messages */
    .status-success {
        background-color: var(--success-bg);
        color: var(--success-text);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid var(--success-border);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .status-success strong {
        color: var(--success-text-strong) !important;
    }
    
    .status-error {
        background-color: var(--error-bg);
        color: var(--error-text);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid var(--error-border);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .status-error strong {
        color: var(--error-text-strong) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid var(--input-border) !important;
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--input-border-focus) !important;
        box-shadow: 0 0 0 1px var(--input-border-focus);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--bg-tertiary);
        transition: background-color 0.3s ease;
    }
    
    /* Metrics styling */
    .css-1xarl3l {
        background-color: var(--bg-primary);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        color: var(--text-primary);
        transition: all 0.3s ease;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: var(--info-bg) !important;
        color: var(--info-text) !important;
        border: 1px solid var(--info-border) !important;
        transition: all 0.3s ease;
    }
    
    .stSuccess {
        background-color: var(--success-bg) !important;
        color: var(--success-text) !important;
        border: 1px solid var(--success-border) !important;
        transition: all 0.3s ease;
    }
    
    .stWarning {
        background-color: var(--warning-bg) !important;
        color: var(--warning-text) !important;
        border: 1px solid var(--warning-border) !important;
        transition: all 0.3s ease;
    }
    
    .stError {
        background-color: var(--error-bg) !important;
        color: var(--error-text) !important;
        border: 1px solid var(--error-border) !important;
        transition: all 0.3s ease;
    }
    
    /* Quick question buttons */
    .quick-question-btn {
        background-color: var(--bg-primary);
        border: 2px solid #6366f1;
        border-radius: 20px;
        padding: 0.8rem 1.2rem;
        margin: 0.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
        color: var(--text-primary) !important;
    }
    
    .quick-question-btn:hover {
        background-color: var(--bg-tertiary);
        border-color: #8b5cf6;
        transform: translateY(-1px);
    }
    
    /* Headers and text visibility */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        transition: color 0.3s ease;
    }
    
    .stMarkdown {
        color: var(--text-primary);
        transition: color 0.3s ease;
    }
    
    /* Ensure all text is readable */
    .stApp .main .block-container {
        color: var(--text-primary);
        transition: color 0.3s ease;
    }
    
    /* Fix metric labels */
    [data-testid="metric-container"] {
        background-color: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        padding: 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"] > div {
        color: var(--text-primary) !important;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
    }
    
    /* File uploader styling */
    .stFileUploader {
        background-color: var(--bg-primary) !important;
        border: 2px dashed #6366f1 !important;
        border-radius: 10px;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader label {
        color: var(--text-primary) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: #6366f1;
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border-color: var(--input-border) !important;
        transition: all 0.3s ease;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border-color: var(--input-border) !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--input-border-focus) !important;
    }
    
    /* Number input styling */
    .stNumberInput > div > div > input {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border-color: var(--input-border) !important;
        transition: all 0.3s ease;
    }
    
    /* Slider styling */
    .stSlider {
        color: var(--text-primary);
        transition: color 0.3s ease;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderContent {
        background-color: var(--bg-secondary) !important;
        border-color: var(--border-color) !important;
        transition: all 0.3s ease;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: var(--bg-primary);
        transition: background-color 0.3s ease;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--bg-primary);
        transition: background-color 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-tertiary) !important;
        transition: color 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--text-primary) !important;
        border-bottom-color: #6366f1;
    }
    
    /* Checkbox and radio styling */
    .stCheckbox > label {
        color: var(--text-primary) !important;
        transition: color 0.3s ease;
    }
    
    .stRadio > label {
        color: var(--text-primary) !important;
        transition: color 0.3s ease;
    }
    
    /* Code block styling */
    .stCode {
        background-color: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        transition: all 0.3s ease;
    }
    
    /* JSON styling */
    .stJson {
        background-color: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease;
    }
    
    /* Additional form elements */
    .stDateInput > div > div > input {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border-color: var(--input-border) !important;
    }
    
    .stTimeInput > div > div > input {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border-color: var(--input-border) !important;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        background-color: var(--input-bg) !important;
        border-color: var(--input-border) !important;
    }
    
    .stMultiSelect > div > div > div {
        color: var(--input-text) !important;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #6366f1 !important;
    }
    
    /* Alert styling */
    .stAlert {
        background-color: var(--info-bg) !important;
        color: var(--info-text) !important;
        border-color: var(--info-border) !important;
    }
</style>
""", unsafe_allow_html=True)

class ChatJeeBot:
    def __init__(self):
        self.pdf_texts = {}
        self.conversation_history = []
        
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from uploaded PDF file"""
        try:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    def create_file_hash(self, file_content: bytes) -> str:
        """Create a hash for the file to avoid reprocessing"""
        return hashlib.md5(file_content).hexdigest()
    
    def process_pdfs(self, uploaded_files) -> Dict[str, str]:
        """Process multiple PDF files and extract text"""
        pdf_texts = {}
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {uploaded_file.name}...")
            
            # Create file hash to check if already processed
            file_content = uploaded_file.read()
            file_hash = self.create_file_hash(file_content)
            
            # Reset file pointer
            uploaded_file.seek(0)
            
            # Extract text
            text = self.extract_text_from_pdf(uploaded_file)
            if text.strip():
                pdf_texts[uploaded_file.name] = {
                    'text': text,
                    'hash': file_hash,
                    'pages': len(PdfReader(uploaded_file).pages)
                }
            
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        status_text.text("✅ All PDFs processed successfully!")
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
        return pdf_texts
    
    def create_context_prompt(self, user_question: str, pdf_texts: Dict) -> str:
        """Create context-aware prompt with PDF content"""
        context = f"""You are "Chat Jee", an expert AI tutor specializing in JEE (Joint Entrance Examination) and competitive exam preparation. You have access to the following study materials:

"""
        
        # Add PDF information to context
        for filename, content in pdf_texts.items():
            context += f"📚 **{filename}** ({content['pages']} pages)\n"
        
        context += f"""

**User Question:** {user_question}

**Instructions:**
- Provide detailed, step-by-step explanations
- Use relevant information from the uploaded study materials when applicable
- Include formulas, concepts, and examples
- Give practical JEE preparation tips
- Reference specific sections or topics from the materials when relevant
- If solving problems, show complete solution steps
- Be encouraging and supportive
- Format mathematical expressions clearly
- For PYQs (Previous Year Questions), provide detailed analysis
- Use proper formatting with headings, bullet points, and numbered steps where appropriate

**Available Study Content:**
"""
        
        # Add relevant text snippets (limited to avoid token limits)
        total_context_length = 0
        max_context_length = 8000  # Adjust based on model limits
        
        for filename, content in pdf_texts.items():
            text_snippet = content['text'][:2000]  # Take first 2000 chars
            if total_context_length + len(text_snippet) < max_context_length:
                context += f"\n--- Content from {filename} ---\n{text_snippet}\n"
                total_context_length += len(text_snippet)
        
        context += "\nPlease provide a comprehensive answer based on the above materials:"
        
        return context
    
    def get_gemini_response(self, prompt: str) -> str:
        """Get response from Gemini using your imported model"""
        try:
            if not GEMINI_AVAILABLE:
                return "❌ Gemini AI module not available. Please check Gemine_AI.py file."
            
            # Add to conversation history for context
            self.conversation_history.append(f"User: {prompt}")
            
            # Create conversation context
            conversation_context = "\n".join(self.conversation_history[-10:])  # Keep last 10 exchanges
            full_prompt = conversation_context + "\nAssistant:"
            
            # Generate response using your imported model
            response = model.generate_content(full_prompt)
            bot_reply = response.text.strip()
            
            # Add bot response to history
            self.conversation_history.append(f"Assistant: {bot_reply}")
            
            return bot_reply
        
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            st.error(error_msg)
            return error_msg

def main():
    # Check if Gemini is available
    if not GEMINI_AVAILABLE:
        st.markdown("""
        <div class="status-error">
            <h3>⚠️ Setup Required</h3>
            <p>Please ensure that <code>Gemine_AI.py</code> is in the same directory as this Streamlit app.</p>
            <p>Your <code>Gemine_AI.py</code> should contain the configured Gemini model.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Initialize the chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = ChatJeeBot()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False
    
    if 'pdf_texts' not in st.session_state:
        st.session_state.pdf_texts = {}
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Chat Jee</h1>
        <p>Your AI-powered JEE & Competitive Exam Assistant</p>
        <p><em>Upload study materials and get intelligent answers!</em></p>
        <p><small>✅ Using your configured AI model</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Show API status
        st.markdown("""
        <div class="status-success">
            <strong>🔑 API Status:</strong> Online
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # File upload
        st.header("📚 Upload Study Materials")
        uploaded_files = st.file_uploader(
            "Upload PDF files (JEE materials, question banks, etc.)",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload multiple PDF files containing JEE study materials"
        )
        
        # Process PDFs button
        if uploaded_files and not st.session_state.pdf_processed:
            if st.button("🚀 Process PDFs", type="primary"):
                with st.spinner("Processing PDFs..."):
                    st.session_state.pdf_texts = st.session_state.chatbot.process_pdfs(uploaded_files)
                    st.session_state.pdf_processed = True
                    st.success("PDFs processed successfully!")
                    st.rerun()
        
        # Display PDF info
        if st.session_state.pdf_texts:
            st.markdown("### 📄 Loaded Materials:")
            for filename, content in st.session_state.pdf_texts.items():
                st.markdown(f"""
                <div class="pdf-info">
                    <strong>{filename}</strong><br>
                    📖 {content['pages']} pages<br>
                    📝 {len(content['text'])} characters
                </div>
                """, unsafe_allow_html=True)
        
        # Reset button
        if st.button("🔄 Reset Session"):
            st.session_state.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        ### 💡 Tips:
        - Upload comprehensive study materials
        - Ask specific questions about topics
        - Request step-by-step solutions
        - Ask for previous year questions
        - Get concept explanations
        - Use mathematical notation in questions
        """)
    
    # Main chat interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Quick question buttons
        st.markdown("### 🚀 Quick Questions:")
        quick_questions = [
            "Explain the concept of limits in calculus with examples",
            "Important topics in Organic Chemistry for JEE Main",
            "Solve a physics problem on rotational motion",
            "Previous year questions on coordinate geometry",
            "Thermodynamics formulas and key concepts",
            "Integration techniques with step-by-step examples"
        ]
        
        cols = st.columns(3)
        for i, question in enumerate(quick_questions):
            with cols[i % 3]:
                if st.button(question, key=f"quick_{i}"):
                    st.session_state.messages.append({"role": "user", "content": question})
                    
                    with st.spinner("Chat Jee is thinking..."):
                        if st.session_state.pdf_texts:
                            context_prompt = st.session_state.chatbot.create_context_prompt(
                                question, st.session_state.pdf_texts
                            )
                        else:
                            context_prompt = f"As Chat Jee, a JEE preparation expert, please answer: {question}"
                        
                        response = st.session_state.chatbot.get_gemini_response(context_prompt)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
        
        st.markdown("---")
        
        # Chat messages
        st.markdown("### 💬 Conversation")
        
        # Display welcome message if no messages
        if not st.session_state.messages:
            st.markdown("""
            <div class="chat-message bot-message">
                <strong>🤖 Chat Jee:</strong><br>
                🎉 Welcome to Chat Jee! I'm ready to help you with JEE preparation. 
                <br><br>
                I can help you with:
                <ul>
                    <li>📚 Concepts from uploaded materials</li>
                    <li>🔍 Problem-solving strategies</li>
                    <li>📝 Previous year questions analysis</li>
                    <li>📖 Topic explanations and examples</li>
                    <li>🧮 Formula derivations and applications</li>
                    <li>💡 Study tips and exam strategies</li>
                </ul>
                <div style="margin-top:1em; padding:0.8em; background: linear-gradient(90deg, #fef08a 0%, #fde68a 100%); border-left:4px solid #f59e0b; border-radius:6px;">
                    <strong style="color:#b8860b;">💡 Pro tip:</strong> 
                    <span style="color:#7c4700;">Upload your study materials first for more accurate and relevant answers!</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display chat messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>🧑‍🎓 You:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🤖 Chat Jee:</strong><br>
                    {message["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_area(
            "Ask me anything about JEE preparation:",
            placeholder="Type your question here... (e.g., 'Explain Newton's laws with examples' or 'Solve this calculus problem step by step')",
            height=100,
            key="user_input"
        )
        
        col_send, col_clear = st.columns([1, 1])
        
        with col_send:
            if st.button("📤 Send Message", type="primary"):
                if not user_input.strip():
                    st.error("Please enter a question!")
                else:
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": user_input})
                    
                    # Get AI response
                    with st.spinner("Chat Jee is thinking..."):
                        if st.session_state.pdf_texts:
                            context_prompt = st.session_state.chatbot.create_context_prompt(
                                user_input, st.session_state.pdf_texts
                            )
                        else:
                            context_prompt = f"As Chat Jee, a JEE preparation expert, please answer: {user_input}"
                        
                        response = st.session_state.chatbot.get_gemini_response(context_prompt)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    st.rerun()
        
        with col_clear:
            if st.button("🗑️ Clear Chat"):
                st.session_state.messages = []
                st.session_state.chatbot.conversation_history = []
                st.rerun()
    
    with col2:
        # Statistics and info
        if st.session_state.pdf_texts:
            st.markdown("### 📊 Session Stats")
            
            total_pages = sum(content['pages'] for content in st.session_state.pdf_texts.values())
            total_chars = sum(len(content['text']) for content in st.session_state.pdf_texts.values())
            
            st.metric("📚 Total PDFs", len(st.session_state.pdf_texts))
            st.metric("📄 Total Pages", total_pages)
            st.metric("💬 Messages", len(st.session_state.messages))
            st.metric("🧠 Context History", len(st.session_state.chatbot.conversation_history))
            
            st.markdown("### 🎯 Study Focus Areas")
            st.info("""
            **Mathematics:**
            - Calculus & Limits
            - Algebra & Functions
            - Coordinate Geometry
            - Trigonometry
            
            **Physics:**
            - Mechanics & Motion
            - Thermodynamics
            - Electromagnetism
            - Modern Physics
            
            **Chemistry:**
            - Organic Chemistry
            - Inorganic Chemistry
            - Physical Chemistry
            - Chemical Bonding
            """)
        
        else:
            st.markdown("### 🔧 Getting Started")
            st.info("""
            **Steps to begin:**
            
            1. ✅ **Gemini AI Ready** (via Gemine_AI.py)
            2. **Upload PDF files** (study materials)
            3. **Process the PDFs**
            4. **Start asking questions!**
            
            📚 **Recommended Materials:**
            - NCERT textbooks (11th & 12th)
            - Previous year JEE papers
            - Reference books (HC Verma, RD Sharma)
            - Formula sheets and notes
            - Topic-wise question banks
            
            💡 **You can ask questions even without PDFs!**
            """)
        
        # Additional features info
        st.markdown("### 🌟 Features")
        st.success("""
        ✅ **PDF Content Analysis**
        ✅ **Context-Aware Responses**
        ✅ **Step-by-Step Solutions**
        ✅ **Conversation Memory**
        ✅ **JEE-Focused Content**
        ✅ **Multi-Subject Support**
        """)

if __name__ == "__main__":
    main()