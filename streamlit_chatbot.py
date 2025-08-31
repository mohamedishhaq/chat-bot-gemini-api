"""
Streamlit Chatbot with Gemini API
Week 2 - Conversational LLMs and Prompt Fundamentals
"""

import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# 🔑 Configure Gemini with hardcoded API key
GEMINI_API_KEY = "AIzaSyDxeeCufoho5j_yQDkG0Qit5c5xOUyhEiM"  # replace with your key
genai.configure(api_key=GEMINI_API_KEY)

# File to store chat history locally
HISTORY_FILE = "chat_history.json"

# Predefined system prompts
SYSTEM_PROMPTS = {
    "Professional Assistant": (
        "You are a professional assistant. Always respond in a formal, polite, "
        "and business-like manner. Use concise sentences, avoid casual phrases, "
        "and provide clear, structured answers suitable for a workplace setting."
    ),
    "Creative Companion": (
        "You are a creative companion. Respond with imaginative, artistic, and "
        "inspiring ideas. Use vivid descriptions, metaphors, and storytelling "
        "elements to make your answers engaging and unique."
    ),
    "Technical Expert": (
        "You are a technical expert. Provide detailed, precise, and well-structured "
        "technical explanations. Include examples, step-by-step reasoning, and "
        "avoid unnecessary fluff. Write in a clear and instructive tone."
    )
}

# Page config
st.set_page_config(page_title=" AI Chat Assistant", page_icon="🤖", layout="wide")

# 🔹 Load chat history from JSON file if exists
if "chat_history" not in st.session_state:
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            st.session_state.chat_history = json.load(f)
    else:
        st.session_state.chat_history = []

# 🔹 Initialize system prompt
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = SYSTEM_PROMPTS["Professional Assistant"]

# 🔹 Initialize chat session
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction=st.session_state.system_prompt
    )
    st.session_state.chat_session = model.start_chat(history=[])

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    persona = st.selectbox("Choose Assistant", list(SYSTEM_PROMPTS.keys()))
    if st.session_state.system_prompt != SYSTEM_PROMPTS[persona]:
        # Reset session when persona changes
        st.session_state.system_prompt = SYSTEM_PROMPTS[persona]
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            system_instruction=st.session_state.system_prompt
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.chat_history = []
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)  # clear local file when persona changes
        st.rerun()

    if st.button("Clear Conversation"):
        model = genai.GenerativeModel(
            "gemini-2.5-flash",
            system_instruction=st.session_state.system_prompt
        )
        st.session_state.chat_session = model.start_chat(history=[])
        st.session_state.chat_history = []
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)  # clear local file
        st.rerun()

    if st.session_state.chat_history:
        export_data = {
            "export_date": datetime.now().isoformat(),
            "system_prompt": st.session_state.system_prompt,
            "conversation": st.session_state.chat_history,
        }
        st.download_button(
            "Download Chat History",
            json.dumps(export_data, indent=2),
            f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "application/json"
        )

# Title
st.title("🤖 AI Chat Assistant")
st.caption("Conversational LLMs & Prompt Engineering")
st.subheader(f"🧑‍💻 Current Persona: {persona}")

# Chat display
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if user_input := st.chat_input("Type your message..."):
    # Save user msg
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chat_session.send_message(user_input)
                reply = response.text.strip()
            except Exception as e:
                reply = f"Error: {str(e)}"
            st.write(reply)

    # Save assistant reply
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # 🔹 Save to local JSON file
    with open(HISTORY_FILE, "w") as f:
        json.dump(st.session_state.chat_history, f, indent=2)

    st.rerun()
