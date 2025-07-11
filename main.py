from keep_alive import keep_alive
import telebot
import os
from datetime import datetime
import time
import requests

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
        reply = f"Your age is: {age_years} years, {age_months} months, and {age_days} days."
    except Exception:
        reply = "❌ Please send date of birth in DD-MM-YYYY format only."

    # --- Error handling & retry logic ---
    for i in range(3):  # 3 baar try karega
        try:
            bot.reply_to(message, reply)
            break  # Agar ho gaya to loop se bahar aa jao
        except requests.exceptions.ConnectionError:
            time.sleep(2)  # 2 second ruk ke fir try karega
        except Exception as e:
            print(f"Error sending message: {e}")
            break  # Agar koi aur error hai to loop band karo

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
