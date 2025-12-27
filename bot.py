import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# Get Keys
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Setup Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Setup Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- FLASK SERVER (For Health Checks) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is healthy", 200

def run_web():
    # Koyeb expects the app to listen on PORT 8000 by default
    app.run(host="0.0.0.0", port=8000)

# --- BOT LOGIC ---
@bot.message_handler(func=lambda m: True)
def reply(message):
    try:
        # Typing action
        bot.send_chat_action(message.chat.id, 'typing')
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Error processing request.")
        print(e)

if __name__ == "__main__":
    # Start Web Server in background
    t = Thread(target=run_web)
    t.start()
    
    # Start Bot
    print("Bot started...")
    bot.infinity_polling()
