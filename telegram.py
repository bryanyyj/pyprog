import RPi.GPIO as GPIO
from keypad_driver import Keypad
import I2C_LCD_driver
from scrolling_display import ScrollingDisplay
from time import sleep
import telepot
from telepot.loop import MessageLoop
from rpi.py import scroll_text_intro

# Setting up the LCD first
LCD = I2C_LCD_driver.lcd()  # Instantiate an LCD object
sleep(0.5)
LCD.backlight(0)  # Turn backlight off
sleep(0.5)
LCD.backlight(1)  # Turn backlight on
LCD.lcd_clear()

# Create an instance of ScrollingDisplay
scrolling_display = ScrollingDisplay(LCD, max_width=16)

# Define your keypad configuration
ROWS = [6, 20, 19, 13]
COLS = [12, 5, 16]
LAYOUT = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ['*', 0, '#']
]

# Initialize the keypad
keypad = Keypad(rows=ROWS, cols=COLS, layout=LAYOUT)

# Telegram bot setup
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

# Start scrolling intro
scroll_text_intro()

# Process orders
while True:
    process_order()

# Cleanup GPIO
GPIO.cleanup()
