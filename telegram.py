import time
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

def send_order_to_telegram(order_id, stall_name, item_name):
    message = f"📢 New Order #{order_id}:\n🍽 Stall: {stall_name}\n🍔 Item: {item_name}\n✅ Reply with /done {order_id} when ready!"
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)
    print("Order sent to Telegram!")

# Handler for order completion (from stall owner)
def mark_order_done(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Usage: /done <order_id>")
        return
    
    order_id = int(context.args[0])
    if order_id in orders:
        # Update LCD and trigger buzzer
        lcd.clear()
        lcd.message = f"Order {order_id}\nReady for pickup!"
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

        update.message.reply_text(f"✅ Order {order_id} is marked as ready!")
        print(f"Order {order_id} marked as ready!")
    else:
        update.message.reply_text("Order not found!")

# Main ordering process
def main():
    
# Start Telegram bot listener
def start_telegram_bot():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("done", mark_order_done))
    updater.start_polling()
    print("Telegram bot listening for /done command...")
