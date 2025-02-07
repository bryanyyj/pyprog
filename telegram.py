from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Telegram Bot Token (replace with yours)
BOT_TOKEN = "7748474537:AAHC3CiNE-WKlpskpqOBWVM5IyTsiHcNrHU"
CHAT_ID = "12345"  # Replace with the chat ID of the recipient

# Telegram API URL to get updates
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

# Send request to Telegram API
response = requests.get(url).json()

# Print the response
print(response)

# Extract the chat_id (if available)
if "result" in response and len(response["result"]) > 0:
    chat_id = response["result"][-1]["message"]["chat"]["id"]
    print(f"Your Chat ID: {chat_id}")
else:
    print("No messages found. Send a message to your bot first.")

