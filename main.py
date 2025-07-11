from keep_alive import keep_alive
import telebot
import os
from datetime import datetime

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Namaste 🙏! Please send your date of birth in DD-MM-YYYY format.")

@bot.message_handler(func=lambda message: True)
def calculate_age(message):
    try:
        dob = datetime.strptime(message.text, "%d-%m-%Y").date()
        today = datetime.today().date()
        age_years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        age_months = (today.month - dob.month) % 12
        age_days = (today - dob.replace(year=today.year)).days if today >= dob.replace(year=today.year) else (today - dob.replace(year=today.year-1)).days
        bot.reply_to(message, f"Your age is: {age_years} years, {age_months} months, and {age_days} days.")
    except:
        bot.reply_to(message, "❌ Please send date in DD-MM-YYYY format only.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
