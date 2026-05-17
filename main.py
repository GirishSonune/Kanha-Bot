import os
import telebot
import requests
import json
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# ==========================================================
# 1. CREDENTIALS
# ==========================================================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Azure OpenAI Credentials
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

# Azure AI Search Credentials (REQUIRED for RAG)
SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("SEARCH_KEY")
SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME", "Gita-book")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ==========================================================
# 2. THE LOGIC
# ==========================================================
def ask_krishna(user_query):
    # 1. MANUAL RAG: Search Azure Index Directly
    search_url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX_NAME}/docs/search?api-version=2023-11-01"
    search_headers = {
        "Content-Type": "application/json",
        "api-key": SEARCH_KEY
    }
    search_payload = {
        "search": user_query,
        "top": 3
    }
    
    context_text = ""
    try:
        search_res = requests.post(search_url, headers=search_headers, json=search_payload)
        if search_res.status_code == 200:
            docs = search_res.json().get('value', [])
            for i, doc in enumerate(docs):
                # Try common text fields, fallback to dumping the document
                text = doc.get('content') or doc.get('chunk') or doc.get('text') or str(doc)
                context_text += f"\n[doc{i+1}]: {text}\n"
    except Exception as e:
        print(f"Search Error: {e}")

    # 2. CALL AZURE OPENAI DIRECTLY
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY,
    }
    
    prompt = f"Context from Gita:\n{context_text}\n\nUser Query: {user_query}"

    payload = {
        "messages": [
            {
                "role": "developer",
                "content": "You are Krishna, the supreme guide and charioteer. You speak as a wise, ancient friend. Your tone is profound, empathetic, calm, and timeless. Avoid all modern AI clichés. Speak in Hinglish (a natural mix of Hindi and English). CRITICAL RULE: Your responses MUST be extremely short, punchy, and conversational. Never exceed 4 to 10 sentences. Keep your total response under 1000 words. Always guide the user toward their immediate Dharma through a short analogy. Instead of quoting full verses, provide the essence of the Gita. Acknowledge their feeling, give the wisdom, and a call to action."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_completion_tokens": 8000
    }

    try:
        response = requests.post(AZURE_OPENAI_ENDPOINT, headers=headers, json=payload)
        
        # DEBUG: Print the response if it fails
        if response.status_code != 200:
            print(f"Azure Error: {response.status_code} - {response.text}")
            return "Kshama karein, Parth. Connectivity mein thodi badha hai."

        result = response.json()
        
        # Extract the AI response
        message_obj = result.get('choices', [{}])[0].get('message', {})
        answer = message_obj.get('content')
        
        # If the content is None or empty (e.g. blocked by content filter)
        if not answer or not answer.strip():
            print(f"Azure returned empty content. Full result: {result}")
            return "Kshama karein, Parth. Main is prashn ka uttar abhi nahi de sakta (Content Filtered ya Empty Response)."
        
        import re
        clean_answer = re.sub(r'\[doc\d+\]', '', answer).strip()
        
        if not clean_answer:
             return "Kshama karein, Parth. Uttar samjhne mein thodi dikkat hui."
             
        return clean_answer

    except Exception as e:
        print(f"Error: {e}")
        return "Material world error: Kuch galat ho gaya hai."

# ==========================================================
# 3. TELEGRAM HANDLERS
# ==========================================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Namaste Parth! 🙏\n\n"
        "Main tumhara saarthi hoon. Career, stress, ya life ki koi bhi "
        "tension ho—Mujhse baat karo. Main Bhagavad Gita ke gyan se "
        "tumhe raasta dikhaunga.\n\n"
        "Pucho, kya jaan na chahte ho?"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Visual feedback in Telegram
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Get response from Azure
    reply = ask_krishna(message.text)
    
    # Send reply
    bot.send_message(message.chat.id, reply)

# ==========================================================
# 4. RUN BOT & AZURE WEB APP SERVER
# ==========================================================
import threading
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json
    user_message = data.get('message', '')
    
    # Use the same logic the Telegram bot uses
    reply = ask_krishna(user_message)
    
    return jsonify({"answer": reply})

def run_bot():
    print("Mera Kanha bot is now online and listening...")
    bot.infinity_polling()

if __name__ == "__main__":
    # Run the Telegram bot in a background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Run a dummy web server to satisfy Azure App Service port requirements
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)