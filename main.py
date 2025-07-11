from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from datetime import datetime
import os

# --- Flask keep-alive server ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Telegram bot handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Namaste 🙏! Please send your date of birth in DD-MM-YYYY format.")

async def calculate_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        dob = datetime.strptime(update.message.text, "%d-%m-%Y").date()
        today = datetime.today().date()
        age_years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        age_months = (today.month - dob.month) % 12
        age_days = (today - dob.replace(year=today.year)).days if today >= dob.replace(year=today.year) else (today - dob.replace(year=today.year-1)).days
        await update.message.reply_text(
            f"Your age is: {age_years} years, {age_months} months, and {age_days} days."
        )
    except:
        await update.message.reply_text("❌ Please send date in DD-MM-YYYY format only.")

# --- Main bot setup ---
async def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("❌ BOT_TOKEN environment variable not set!")
        return

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate_age))

    print("🤖 Bot is starting...")
    await application.run_polling()

# --- Run everything ---
if __name__ == "__main__":
    keep_alive()
    import asyncio
    asyncio.run(main())
