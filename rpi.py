import RPi.GPIO as GPIO
from keypad_driver import Keypad
import I2C_LCD_driver
from scrolling_display import ScrollingDisplay
from time import sleep

# Setting up the LCD first
LCD = I2C_LCD_driver.lcd()  # Instantiate an LCD object, call it LCD
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

def scroll_text_intro():
    key = None
    text1 = "Welcome to the canteen POS,"
    text2 = "Press 0 to start your order!"
    duration_per_shift = 0.3  # Adjust duration per shift here

    while key != 0:
        key = keypad.get_last_key()  # Get the last key pressed
        scrolling_display.scroll_texts(text1, text2, duration_per_shift)  # Scroll the texts

        if key == 0:  # If '0' is pressed
            LCD.lcd_clear()  # Clear the display
            return  # Exit the scrolling function

# Start scrolling texts
scroll_text_intro()

# After stopping the scrolling, display the ordering menu
LCD.lcd_display_string("Ordering menu", 1)
sleep(20)  # Hold the message for 20 seconds

# Cleanup GPIO and exit
GPIO.cleanup()
