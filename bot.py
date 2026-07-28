import os
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Render ነፃ ዕቅድ ላይ Timed out እንዳይል አነስተኛ Web Server ማዘጋጀት
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot status: Alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# Environment Variables
GEMINI_API_KEY = os.environ.get("AQ.Ab8RN6KPpy4xhKy5SezWy9sm4qj2SHavuHIGF2S8hsdLNPdbAw")
TELEGRAM_TOKEN = os.environ.get("8751618578:AAEsSu2QzbWEQ-YlmgnqgCPc3RhKeVFRgYY")

# Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! እኔ AI ረዳትህ ነኝ። ማንኛውንም ጥያቄ መጠየቅ ትችላለህ!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_chat_action("typing")
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text,
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("ይቅርታ፣ ከ Gemini AI ጋር መገናኘት አልተቻለም። እባክህ Render ላይ GEMINI_API_KEY ትክክል መሆኑን አረጋግጥ።")

def main():
    keep_alive()  # Web server በማስነሳት Render ን ሰርቪሱ ክፍት እንደሆነ እንዲያውቅ ያደርጋል
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("ቦቱ መስራት ጀምሯል...")
    app.run_polling()

if __name__ == "__main__":
    main()


