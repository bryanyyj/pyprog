import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your bot token and chat ID
BOT_TOKEN = "7823253969:AAEYvW89aQ3a5ozS2rhJmpEAy-hv7q-a-sM"
CHAT_ID = "1874241047"

def send_order_to_stall(order_details,order_id):
    """Sends the current order for stall 1 through Telegram."""
    MESSAGE = f"Current Order for Stall 1:\n{order_details}\nID: {order_id}"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": MESSAGE}

    try:
        response = requests.post(url, data=data)
        response_data = response.json()  # Check the response

        if response_data.get("ok"):
            logger.info("Order sent successfully!")
        else:
            logger.error(f"Failed to send message: {response_data.get('description')}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending message: {e}")
    