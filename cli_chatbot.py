"""
CLI Chatbot with Gemini API
Week 2 - Conversational LLMs and Prompt Fundamentals
"""

import google.generativeai as genai
import os

GEMINI_API_KEY = "your_api_key_here"

if not GEMINI_API_KEY:
    raise ValueError("Please set the GEMINI_API_KEY environment variable or hardcode it in the script.")

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)

# === System Prompts (Personas) ===
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

def chat_loop():
    print("=== Gemini CLI Chatbot ===")
    print("Choose a persona:")
    for i, persona in enumerate(SYSTEM_PROMPTS.keys(), 1):
        print(f"{i}. {persona}")
    
    choice = input("Enter number (1-3): ").strip()
    persona = list(SYSTEM_PROMPTS.keys())[int(choice)-1]
    system_prompt = SYSTEM_PROMPTS[persona]

    print(f"\nPersona selected: {persona}")
    print("Type 'exit' to quit.\n")

    # Initialize conversation history
    history = [{"role": "user", "parts": f"System instruction: {system_prompt}"}]
    model = genai.GenerativeModel("gemini-2.5-flash")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting chat...")
            break

        # Add user input
        history.append({"role": "user", "parts": user_input})

        try:
            response = model.generate_content(history)
            reply = response.text.strip()
        except Exception as e:
            reply = f"Error: {str(e)}"

        print(f"{persona}: {reply}\n")

        # Add assistant reply
        history.append({"role": "model", "parts": reply})

if __name__ == "__main__":
    chat_loop()
