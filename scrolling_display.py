import time
import I2C_LCD_driver
import keypad_driver

class LCDKeypad:
    def __init__(self, row_pins, col_pins, keypad_layout):
        self.lcd = I2C_LCD_driver.lcd()
        self.keypad = keypad_driver.Keypad(row_pins, col_pins, keypad_layout)
    
    def scroll_texts_for_keypress(self, text1, text2, duration_per_shift=0.3, cycles=5):
        """
        Scrolls text on the LCD display and waits for a keypress to return the key.
        """
        text1 += " " * 16  # Ensure spacing for smooth scrolling
        text2 += " " * 16
        
        scroll_length = max(len(text1), len(text2))
        
        while True:
            for _ in range(cycles):
                for i in range(scroll_length - 15):  # Ensure full display of long texts
                    display_text1 = text1[i:i+16].ljust(16)  # Ensure fixed 16-char display
                    display_text2 = text2[i:i+16].ljust(16)
                    
                    self.lcd.lcd_display_string(display_text1, 1)
                    self.lcd.lcd_display_string(display_text2, 2)
                    
                    time.sleep(duration_per_shift)
                    self.lcd.lcd_clear()
                    
                    key = self.keypad.get_last_key()
                    if key:
                        return key

# Example usage (if running standalone)
if __name__ == "__main__":
    ROW_PINS = [5, 6, 13, 19]
    COL_PINS = [12, 16, 20, 21]
    KEYPAD_LAYOUT = [
        ['1', '2', '3'],
        ['4', '5', '6'],
        ['7', '8', '9'],
        ['*', '0', '#']
    ]
    
    lcd_keypad = LCDKeypad(ROW_PINS, COL_PINS, KEYPAD_LAYOUT)
    key_pressed = lcd_keypad.scroll_texts_for_keypress("Hello, this is a longer test message!", "Press any key to continue.")
    print("Key Pressed:", key_pressed)
