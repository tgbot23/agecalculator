from keep_alive import keep_alive
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
import os

def start(update, context):
    update.message.reply_text("Namaste 🙏! Please send your date of birth in DD-MM-YYYY format.")

def calculate_age(update, context):
    try:
        dob = datetime.strptime(update.message.text, "%d-%m-%Y").date()
        today = datetime.today().date()
        age_years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        age_months = (today.month - dob.month) % 12
        age_days = (today - dob.replace(year=today.year)).days if today >= dob.replace(year=today.year) else (today - dob.replace(year=today.year-1)).days
        update.message.reply_text(f"Your age is: {age_years} years, {age_months} months, and {age_days} days.")
    except:
        update.message.reply_text("❌ Please send date in DD-MM-YYYY format only.")

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("❌ BOT_TOKEN environment variable not set!")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, calculate_age))

    print("🤖 Bot is starting...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    keep_alive()
    main()
