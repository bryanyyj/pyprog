import RPi.GPIO as GPIO
from keypad_driver import Keypad
import I2C_LCD_driver
from time import sleep

# Setting up the LCD
LCD = I2C_LCD_driver.lcd()
LCD.lcd_clear()

# Keypad configuration
ROWS = [6, 20, 19, 13]
COLS = [12, 5, 16]
LAYOUT = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ['*', 0, '#']
]
keypad = Keypad(rows=ROWS, cols=COLS, layout=LAYOUT)

# Stalls and menu items
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
    5: {1: ("Briyani", 5.50), 2: ("Rendang", 4.50)}
}

# Menu navigation
def display_stall_menu():
    current_stall = 1
    while True:
        # Display current stall
        LCD.lcd_clear()
        LCD.lcd_display_string(f"Stall: {stalls[current_stall]}", 1)
        LCD.lcd_display_string("Press # to select", 2)

        key = keypad.get_last_key()
        if key == '*':  # Go back
            current_stall = current_stall - 1 if current_stall > 1 else len(stalls)
        elif key == '#':  # Select stall
            display_menu(current_stall)
        elif key == 0:  # Exit
            LCD.lcd_clear()
            LCD.lcd_display_string("Exiting Menu", 1)
            sleep(2)
            return
        else:  # Scroll forward
            current_stall = current_stall + 1 if current_stall < len(stalls) else 1
        sleep(0.2)

def display_menu(stall_id):
    current_item = 1
    while True:
        # Display menu item
        menu = menus[stall_id]
        item_name, item_price = menu[current_item]
        LCD.lcd_clear()
        LCD.lcd_display_string(f"{item_name} ${item_price:.2f}", 1)
        LCD.lcd_display_string("Press # to order", 2)

        key = keypad.get_last_key()
        if key == '*':  # Go back
            current_item = current_item - 1 if current_item > 1 else len(menu)
        elif key == '#':  # Place order
            LCD.lcd_clear()
            LCD.lcd_display_string(f"Ordered: {item_name}", 1)
            sleep(2)
            return
        elif key == 0:  # Exit
            LCD.lcd_clear()
            LCD.lcd_display_string("Exiting Menu", 1)
            sleep(2)
            return
        else:  # Scroll forward
            current_item = current_item + 1 if current_item < len(menu) else 1
        sleep(0.2)

# Run the menu system
try:
    display_stall_menu()
finally:
    GPIO.cleanup()
