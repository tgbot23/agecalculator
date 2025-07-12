from keep_alive import keep_alive
import telebot
import os
import time
import requests
from datetime import date
from dateutil import parser
from dateutil.relativedelta import relativedelta

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Namaste 🙏! Please send your Date of Birth (DOB) in any format.\n\nExamples:\n👉 1 Jan 2000\n👉 01/01/1999\n👉 01-01-1898")

@bot.message_handler(func=lambda message: True)
def calculate_age(message):
    user_input = message.text.strip()
    try:
        dob = parser.parse(user_input, dayfirst=True).date()
        today = date.today()

        if dob > today:
            reply = "❌ Aap future date nahi bhej sakte. DOB dobara bhejein."
        else:
            diff = relativedelta(today, dob)
            reply = f"🎉 Your age is: {diff.years} years, {diff.months} months, and {diff.days} days."
    except Exception:
        reply = "❌ Sorry, date samajh nahi aayi. Kripya DOB dobara bhejein (jaise: 1 Jan 2000 ya 01-01-1999)."

    for i in range(3):  # 3 baar try karega
        try:
            bot.reply_to(message, reply)
            break
        except requests.exceptions.ConnectionError:
            time.sleep(2)
        except Exception as e:
            print(f"Error sending message: {e}")
            break

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
