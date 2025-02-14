import time
import I2C_LCD_driver as lcd
import keypad_driver as Keypad

# Define GPIO pins for rows and columns
ROW_PINS = [5, 6, 13, 19]  # Example row pins
COL_PINS = [12, 16, 20, 21]  # Example column pins

# Define keypad layout (4x4 example)
KEYPAD_LAYOUT = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Create keypad instance
keypad = Keypad(ROW_PINS, COL_PINS, KEYPAD_LAYOUT)




def scroll_texts_for_keypress(text1, text2, duration_per_shift=0.3, cycles=5):

    # Repeat the text enough times to at least fill 16 characters
    while len(text1) < 16:
        text1 += text1  # Repeat itself until it’s at least 16 characters
    while len(text2) < 16:
        text2 += text2

    # Ensure we only take the needed portion
    text1 = text1[:16] + " " + text1[:16]  # Creates a smooth loop effect
    text2 = text2[:16] + " " + text2[:16]

    scroll_length = len(text1)  # Get the length of the scrolling window
    while True:
        for _ in range(cycles):  # Limit number of cycles
            for i in range(scroll_length):
                display_text1 = text1[i:i+16]  # Take a 16-character window
                display_text2 = text2[i:i+16]

                # Display on LCD
                lcd.lcd_display_string(display_text1, 1)
                lcd.lcd_display_string(display_text2, 2)

                time.sleep(duration_per_shift)
                lcd.lcd_clear()
                key = keypad.get_last_key()
                if key:
                    return key
