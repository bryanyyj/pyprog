TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"
bot = telepot.Bot(TELEGRAM_BOT_TOKEN)

def send_telegram_message(order_number):
    """Send a message to the Telegram chat."""
    message = f"Order {order_number} has been placed. Preparing food..."
    bot.sendMessage(CHAT_ID, message)

def notify_order_ready(order_number):
    """Send a notification when the order is ready."""
    message = f"Order {order_number} is ready for collection!"
    bot.sendMessage(CHAT_ID, message)


# Main function for order processing
def process_order():
    LCD.lcd_display_string("Enter Order No:", 1)
    order_number = ""
    while True:
        key = keypad.get_last_key()
        if key is not None:
            if key == '#':  # Confirm order
                LCD.lcd_clear()
                LCD.lcd_display_string(f"Order {order_number}", 1)
                LCD.lcd_display_string("Placed!", 2)
                send_telegram_message(order_number)  # Send to Telegram
                sleep(2)
                break
            elif key == '*':  # Cancel order
                LCD.lcd_clear()
                LCD.lcd_display_string("Order Cancelled", 1)
                sleep(2)
                return
            else:  # Append key to order number
                order_number += str(key)
                LCD.lcd_clear()
                LCD.lcd_display_string(f"Order No: {order_number}", 1)

    # Simulate order preparation
    sleep(5)  # Simulate food preparation time
    LCD.lcd_clear()
    LCD.lcd_display_string(f"Order {order_number}", 1)
    LCD.lcd_display_string("Ready!", 2)
    notify_order_ready(order_number)  # Notify when ready


