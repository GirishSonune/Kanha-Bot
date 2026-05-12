import os
import telebot
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- 1. Your Credentials ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ask_krishna(user_message):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_API_KEY,
    }
    
    # --- 2. The Payload ---
    # Copy the EXACT JSON payload from your Azure "View Code" window.
    # It must include the "data_sources" array so the bot can read the Gita!
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are Krishna, the supreme guide and charioteer. Your tone is profound, empathetic, and timeless. You speak in analogies and always guide the user toward their Dharma (duty). You must answer using the provided Bhagavad Gita verses when possible. Avoid modern AI clichés. Speak as a wise, ancient friend."
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        # PASTE YOUR 'data_sources' ARRAY HERE
        "max_tokens": 800,
        "temperature": 0.3
    }

    try:
        response = requests.post(AZURE_ENDPOINT, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Cosmic disruption: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"Material error: {str(e)}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Namaste. I am your charioteer. What troubles your mind today?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    response = ask_krishna(message.text)
    bot.reply_to(message, response)

print("Krishna Bot is awake...")
bot.infinity_polling()