# 🤖 Gemini Chatbot Suite
**Week 2 - Conversational LLMs and Prompt Fundamentals**

This project provides two chatbot implementations powered by **Google’s Gemini API**:

- **CLI Chatbot (`cli_chatbot.py`)** – interact via the terminal.  
- **Streamlit Chatbot (`streamlit_chatbot.py`)** – interactive web-based chat UI.  

Both versions support **multiple personas**:  
- 🧑‍💼 *Professional Assistant* – formal & business-like responses  
- 🎨 *Creative Companion* – imaginative & artistic answers  
- 🛠️ *Technical Expert* – precise, detailed technical explanations  

---

## 📂 Project Structure

  ├── cli_chatbot.py # Command-line chatbot
  ├── streamlit_chatbot.py # Streamlit web chatbot
  ├── requirements.txt # Python dependencies
  ├── chat_history.json # Saved conversation history (created at runtime)
  └── README.md # Project documentation


---

## ⚡ Features

- Multiple **chat personas** with predefined system prompts  
- **CLI mode** for lightweight terminal interaction  
- **Streamlit web app** with sidebar controls  
  - Persona selection  
  - Clear conversation  
  - Download chat history (JSON)  
- **Conversation persistence** (saves locally in `chat_history.json`)  

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/gemini-chatbot.git
cd gemini-chatbot

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

On Linux / macOS:
export GEMINI_API_KEY="your_api_key_here"

On Windows (PowerShell):
$env:GEMINI_API_KEY="your_api_key_here"

CLI Chatbot
python cli_chatbot.py

Streamlit Chatbot
streamlit run streamlit_chatbot.py


