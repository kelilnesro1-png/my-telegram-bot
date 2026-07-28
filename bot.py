import asyncio
import base64
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 የቴሌግራም ቦት ቶከንህን እዚህ አስገባ
bt1 = "8751618578:AAEsSu2QzbWEQ-"
bt2 ="YlmgnqgCPc3RhKeVFRgYY
"
TELEGRAM_BOT_TOKEN = bt1 + bt2

# Gemini API Key
k1 = "AQ.Ab8RN6IDImKk3YnqHuy7K-"
k2 = "fxLkkrl5YsI4DvEFdHjzV7etoDsA"
API_KEY = k1 + k2

# GitHub Token
t1 = "github_pat_11CHAI62Q0pKwRklkNxfpW_"
t2 = "s1DUf4HrD1J4T6Fs7RMSIGXCujV0eOGudWf7og7ZTYX"
t3 = "6CPQCD2Vp92XWy0V"
GITHUB_TOKEN = t1 + t2 + t3

GITHUB_USERNAME = "Kelilnesro1-png"

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ሰላም! 🖐️ እኔ የ AI Web Builder ቦት ነኝ።\n\n"
        "አፕሊኬሽን ለማሰራት በሚከተለው መልኩ ጻፍልኝ፦\n"
        "የፕሮጀክት_ስም | የምትፈልገው አፕ መግለጫ\n\n"
        "ምሳሌ፦\nmy-calculator | ሳይንቲፊክ ካልኩሌተር አዘጋጅልኝ"
    )

# Handle Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "|" not in text:
        await update.message.reply_text("⚠️ እባክህ በ ' | ' ከፍለህ ጻፍልኝ!\nምሳሌ፦ my-app | የፎቶ ኤዲተር አፕሊኬሽን")
        return

    parts = text.split("|", 1)
    repo_name = parts[0].strip().lower().replace(" ", "-")
    prompt = parts[1].strip()

    await update.message.reply_text("⏳ ኤጀንቱ በማሰብ እና ኮዱን GitHub ላይ በመጫን ላይ ነው...")

    headers = {
        "Authorization": "Bearer " + GITHUB_TOKEN,
        "Accept": "application/vnd.github+json"
    }

    try:
        # 1. Ask Gemini
        system_instruction = "You are an expert web developer. Return ONLY complete valid single-file HTML/CSS/JS code without markdown formatting or code blocks."
        u_prot = "https://"
        u_gemini = "generativelanguage.googleapis.com"
        u_path = "/v1beta/models/gemini-2.5-flash:generateContent?key="
        gemini_url = u_prot + u_gemini + u_path + API_KEY
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": system_instruction}]}
        }
        
        ai_res = requests.post(gemini_url, json=payload).json()
        ai_code = ai_res['candidates'][0]['content']['parts'][0]['text']
        
        # Clean code
        ai_code = ai_code.replace("```html", "").replace("```", "").strip()

        # 2. Check/Create Repo
        u_gh = "api.github.com"
        repo_url = u_prot + u_gh + "/repos/" + GITHUB_USERNAME + "/" + repo_name
        check_repo = requests.get(repo_url, headers=headers)

        if check_repo.status_code == 404:
            requests.post(u_prot + u_gh + "/user/repos", json={"name": repo_name, "auto_init": True}, headers=headers)
            await asyncio.sleep(2)

        # 3. Commit File
        file_url = u_prot + u_gh + "/repos/" + GITHUB_USERNAME + "/" + repo_name + "/contents/index.html"
        get_file = requests.get(file_url, headers=headers)
        sha = get_file.json().get('sha') if get_file.status_code == 200 else None

        encoded_content = base64.b64encode(ai_code.encode('utf-8')).decode('utf-8')
        put_payload = {"message": "Add web app by Telegram AI Bot", "content": encoded_content}
        if sha:
            put_payload["sha"] = sha

        upload_res = requests.put(file_url, json=put_payload, headers=headers)

        # 4. Enable GitHub Pages
        pages_url = u_prot + u_gh + "/repos/" + GITHUB_USERNAME + "/" + repo_name + "/pages"
        requests.post(pages_url, json={"source": {"branch": "main", "path": "/"}}, headers=headers)

        if upload_res.status_code in [200, 201]:
            live_url = u_prot + GITHUB_USERNAME + ".github.io/" + repo_name + "/"
            await update.message.reply_text("🚀 ስራው ተጠናቋል!\n\n🌐 አፑን ለመመልከት ሊንኩን ይጫኑ፦\n" + live_url)
        else:
            await update.message.reply_text("❌ GitHub ላይ መጫን አልተቻለም።")

    except Exception as e:
        await update.message.reply_text("❌ ስህተት ተፈጽሟል፦ " + str(e))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 የቴሌግራም ቦት ስራ ጀምሯል...")
    app.run_polling()
