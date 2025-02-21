import json
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your bot token
TELEGRAM_BOT_TOKEN = "7823253969:AAEYvW89aQ3a5ozS2rhJmpEAy-hv7q-a-sM"


# File to store messages
JSON_FILE = 'display.json'

def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message when the command /start is issued."""
    update.message.reply_text('Welcome! Send me a message and I will save it.')

def save_message_to_json(message: str) -> None:
    """Saves a message to a JSON file."""
    # Load existing messages
    try:
        with open(JSON_FILE, 'r') as file:
            messages = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messages = []

    # Append new message
    messages.append({"message": message})

    # Write back to the JSON file
    with open(JSON_FILE, 'w') as file:
        json.dump(messages, file, indent=4)

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handles incoming messages and saves them to a JSON file."""
    user_message = update.message.text
    logger.info(f"Received message: {user_message}")
    
    # Save the message to JSON
    save_message_to_json(user_message)
    
    # Send confirmation to the user
    update.message.reply_text('Your message has been saved!')

def main() -> None:
    """Starts the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher

    # Add command handler for /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Add message handler for text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start polling for updates
    updater.start_polling()

    # Run the bot until you send a signal to stop (Ctrl+C)
    updater.idle()

if __name__ == '__main__':
    main()
