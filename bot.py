
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# Gemini API እና Telegram Bot Token ማስገቢያ
GEMINI_API_KEY = "AQ.Ab8RN6Ls6_F8BJ6l268HFteRL5_Fe8KxqVh_26vm3jKhiQbHJA"
TELEGRAM_TOKEN = "8751618578:AAEsSu2QzbWEQ-YlmgnqgCPc3RhKeVFRgYY"

# Gemini AI Client ማዘጋጀት
client = genai.Client(api_key=GEMINI_API_KEY)

# /start ትእዛዝ ሲላክ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! እኔ AI ረዳትህ ነኝ። ማንኛውንም ጥያቄ መጠየቅ ትችላለህ!")

# ማንኛውም መልእክት (ጥያቄ) ሲላክ በ AI መመለሻ
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # ለተጠቃሚው AIው እያሰበ መሆኑን ለማሳወቅ
    await update.message.reply_chat_action("typing")
    
    try:
        # Gemini AIን ጥያቄውን መጠየቅ
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
        )
        # የ AIውን መልስ ለተጠቃሚው መላክ
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("ይቅርታ፣ ጥያቄህን ለማቀናበር ስህተት ተፈጥሯል።")

def main():
    # ቦቱን ማስነሳት
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("ቦቱ መስራት ጀምሯል...")
    app.run_polling()

if __name__ == "__main__":
    main()
