import RPi.GPIO as GPIO
import time
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import board
import digitalio
import adafruit_character_lcd.character_lcd_i2c as character_lcd

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



# GPIO Pins for Keypad
ROWS = [5, 6, 13, 19]
COLS = [12, 16, 20, 21]

# GPIO Pin for Buzzer
BUZZER_PIN = 23

# LCD Setup
lcd_columns = 16
lcd_rows = 2
i2c = board.I2C()  # Uses board.SCL and board.SDA
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

# Keypad Layout (4x4 matrix)
KEYPAD = [
    [1, 2, 3, "A"],
    [4, 5, 6, "B"],
    [7, 8, 9, "C"],
    ["*", 0, "#", "D"]
]

# Define stalls and menus
stalls = {
    1: "Drinks",
    2: "Snacks",
    3: "Chicken Rice",
    4: "Western",
    5: "Halal"
}

menus = {
    1: {1: ("Milo", 1.50), 2: ("Juice", 1.50), 3: ("Water", 1.00)},
    2: {1: ("Luo Mi Gao", 2.00), 2: ("Cookies", 1.50), 3: ("Sandwich", 1.00)},
    3: {1: ("Chicken Rice", 5.00), 2: ("Chicken Soup", 3.50)},
    4: {1: ("Baked Rice", 5.00), 2: ("Burger", 4.00), 3: ("Fries", 2.00)},
    5: {1: ("Briyanni", 5.50), 2: ("Rendang", 4.50)}
}

# Orders dictionary to track orders
orders = {}

# Initialize GPIO for keypad
def setup_keypad():
    GPIO.setmode(GPIO.BCM)
    for row in ROWS:
        GPIO.setup(row, GPIO.OUT)
        GPIO.output(row, GPIO.LOW)
    for col in COLS:
        GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Read keypad input
def read_keypad():
    setup_keypad()
    while True:
        for row_index, row in enumerate(ROWS):
            GPIO.output(row, GPIO.HIGH)
            for col_index, col in enumerate(COLS):
                if GPIO.input(col) == GPIO.LOW:
                    GPIO.output(row, GPIO.LOW)
                    return KEYPAD[row_index][col_index]
            GPIO.output(row, GPIO.LOW)
        time.sleep(0.1)

# Send order details to Telegram
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
    GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)

    print("\n=== Welcome to the Canteen Ordering System ===")
    print("Select a stall:")
    for key, name in stalls.items():
        print(f"{key}: {name}")

    # Select stall
    stall_id = None
    while stall_id not in stalls:
        stall_id = read_keypad()
        if isinstance(stall_id, int) and stall_id in stalls:
            print(f"Selected: {stalls[stall_id]}")
        else:
            print("Invalid selection. Try again.")

    print("\nSelect menu item:")
    for key, (name, price) in menus[stall_id].items():
        print(f"{key}: {name} - ${price:.2f}")

    # Select menu item
    item_id = None
    while item_id not in menus[stall_id]:
        item_id = read_keypad()
        if isinstance(item_id, int) and item_id in menus[stall_id]:
            item_name, _ = menus[stall_id][item_id]
            print(f"Added: {item_name}")
        else:
            print("Invalid selection. Try again.")

    # Confirm order
    print("\nPress '#' to confirm order or '*' to cancel.")
    confirm = None
    while confirm not in ["#", "*"]:
        confirm = read_keypad()
    
    if confirm == "#":
        order_id = int(time.time())  # Unique order ID
        orders[order_id] = (stalls[stall_id], item_name)
        send_order_to_telegram(order_id, stalls[stall_id], item_name)
        print("✅ Order confirmed and sent!")
    else:
        print("❌ Order cancelled.")

# Start Telegram bot listener
def start_telegram_bot():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("done", mark_order_done))
    updater.start_polling()
    print("Telegram bot listening for /done command...")

if __name__ == "__main__":
    # Start the bot in a separate thread
    import threading
    threading.Thread(target=start_telegram_bot, daemon=True).start()

    # Run the ordering system
    main()
