import time
import I2C_LCD_driver

lcd = I2C_LCD_driver.lcd()
lcd.lcd_clear()

def scroll_texts(text1, text2, duration_per_shift=0.3, cycles=5):
    """
    Scrolls two lines of text on a 16-character LCD display.

    Parameters:
    text1 (str): Text for the first line.
    text2 (str): Text for the second line.
    duration_per_shift (float): Time delay per shift (default: 0.3s).
    cycles (int): Number of complete scrolling cycles before stopping (default: 5).
    """

    # Repeat the text enough times to at least fill 16 characters
    while len(text1) < 16:
        text1 += text1  # Repeat itself until it’s at least 16 characters
    while len(text2) < 16:
        text2 += text2

    # Ensure we only take the needed portion
    text1 = text1[:16] + " " + text1[:16]  # Creates a smooth loop effect
    text2 = text2[:16] + " " + text2[:16]

    scroll_length = len(text1)  # Get the length of the scrolling window

    for _ in range(cycles):  # Limit number of cycles
        for i in range(scroll_length):
            display_text1 = text1[i:i+16]  # Take a 16-character window
            display_text2 = text2[i:i+16]

            # Display on LCD
            lcd.lcd_display_string(display_text1, 1)
            lcd.lcd_display_string(display_text2, 2)

            time.sleep(duration_per_shift)
            lcd.lcd_clear()

# Example usage
scroll_texts("Hello", "World", duration_per_shift=0.3, cycles=3)
