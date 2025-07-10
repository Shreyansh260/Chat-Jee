# 🎓 Chat Jee – Your AI-Powered JEE Study Assistant

**Chat Jee** is an intelligent AI chatbot built to assist JEE (Joint Entrance Examination) aspirants. Powered by Google Gemini and Streamlit, it provides detailed, context-aware answers to questions from uploaded study materials including NCERTs, PYQs, and reference books. 📘📐

---

## 🚀 Features

✅ Upload PDF study materials (books, notes, PYQs)  
✅ Contextual answers based on uploaded content  
✅ Step-by-step problem-solving in Physics, Chemistry, and Math  
✅ Built-in conversation memory for a seamless experience  
✅ Supports multiple PDFs and smart material processing  
✅ Attractive UI with Light/Dark Theme Adaptation  
✅ Ready-to-use Gemini integration (via `Gemine_AI.py`)  

---

## 📸 Screenshots 

### Chat Jee Screenshot ![Screenshot (554)](https://github.com/user-attachments/assets/d2d7fc8a-50f6-4450-9a76-727fbf1d5353)
### Promtpt Gaving Interferance ![Screenshot (555)](https://github.com/user-attachments/assets/d64232bf-8447-4f41-aaa5-ee644f598fce)
### Uploading Files ![Screenshot (556)](https://github.com/user-attachments/assets/c5fa67fc-6057-42d4-b785-6d99d652839e)
### After Uploading Ask Question ![Screenshot (558)](https://github.com/user-attachments/assets/efee8ef3-043c-438d-aefa-1c0040266da5)
### Gave Answers According to File and inteligence ![Screenshot (559)](https://github.com/user-attachments/assets/9b380a44-72e8-4f18-a34b-751f55154c74)
### Covers all the important formullas and topics ![Screenshot (560)](https://github.com/user-attachments/assets/a2f7a278-3cdf-4b9f-bc75-c48ae00778bd)
![Screenshot (561)](https://github.com/user-attachments/assets/4cefc8b1-a3f5-46fc-aea7-56d8496a32a0)
![Screenshot (562)](https://github.com/user-attachments/assets/bb24c6bb-9519-4b29-8b51-527a2e0099db)









---

## 🧠 Technologies Used

- **Python** 🐍  
- **Streamlit** – Web app framework  
- **Google Gemini API** (via `Gemine_AI.py`)  
- **PyPDF2** – For extracting text from PDFs  
- **Custom CSS** – For sleek dark/light UI themes  

---

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/chat-jee.git
   cd chat-jee
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gemini AI model**
   - Make sure you have a file named `Gemine_AI.py` in the same directory.
   - It should contain your configured Gemini model object (e.g., `model = genai.GenerativeModel(...)`).

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## 📚 How to Use

1. Upload your JEE materials in PDF format (books, notes, etc.)
2. Click "Process PDFs" to extract and analyze the content
3. Ask your questions via the chat box or use quick buttons
4. Get intelligent, accurate, and exam-oriented answers from Chat Jee 🤖

---

## 📁 Folder Structure

```
chat-jee/
│
├── app.py                # Main Streamlit app
├── Gemine_AI.py          # Gemini API model setup (required)
├── requirements.txt      # Python dependencies
└── README.md             # You're reading it!
```

---

## ✨ Pro Tips

- Use specific questions like "Explain limits with graphs" or "Solve this thermodynamics question step by step"
- Upload full NCERT books, PYQs, and handwritten notes to get the most relevant answers
- Chat Jee also supports formulas, concept breakdowns, and exam tips! 💡

---

## 🚀 Future Add-ons for *Chat Jee*

### 🧠 1. **Voice Input & Output**
- Let users **ask questions via microphone**
- Read the AI's response out loud using **Text-to-Speech (TTS)**
- 📦 Libraries: `speechrecognition`, `gTTS`, `pyttsx3`

### 📝 2. **Math Equation Support (LaTeX Renderer)**
- Support math questions with clean **LaTeX-style rendering**
- Let users write: `\int x^2 dx` and show it beautifully in UI
- 📦 Use: `MathJax`, Streamlit's `st.latex()`

### 🧾 3. **In-App MCQ Practice Mode**
- Add a quiz/practice mode with **multiple-choice questions**
- Include timer ⏱, progress bar, and performance stats

### 🧠 4. **Offline Mode with Local LLM (e.g., Mistral, LLaMA)**
- Allow the bot to run **without internet**, using a local model via `transformers`
- 📦 Hugging Face + quantized LLM

### 📚 5. **OCR Support for Handwritten Notes**
- Allow users to upload **scanned handwritten notes or images**
- Extract text using OCR (Optical Character Recognition)
- 📦 Use: `pytesseract`, `opencv-python`

### 📈 6. **Smart Progress Tracker**
- Let users **track topics covered**, weak areas, and generate weekly reports
- Show charts using `plotly` or `matplotlib`

### 📅 7. **Custom Study Planner Generator**
- Generate a **JEE-focused study plan** based on syllabus, remaining time, and weak topics

### 🧩 8. **Interactive Concept Maps**
- Show visual maps of linked topics (e.g., Thermodynamics → Laws → Applications)
- Great for **revising complex chapters**

### 🌐 9. **Multilingual Support**
- Answer questions in **Hindi or Hinglish** for better accessibility

### 💬 10. **Telegram/WhatsApp Bot Integration**
- Let users chat with **Chat Jee on mobile** directly from Telegram or WhatsApp
---

## 📬 Contact

Made with ❤️ by **Shriyansh Singh Rathore**

📧 Email: shreyanshsinghrathore7@gmail.com

---

## 📄 License

This project is open-source and available under the MIT License.
