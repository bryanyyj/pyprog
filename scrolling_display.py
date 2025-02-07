import time
import math
class ScrollingDisplay:
    def __init__(self, lcd, max_width):
        self.lcd = lcd
        self.max_width = max_width

    def scroll_texts(self, text1, text2, duration_per_shift=0.3):
        text1 = text1 + " " 
        text2 = text2 + " "  
        text1_length = len(text1)
        text2_length = len(text2)
        
 
        loop_index = abs(text1_length * text2_length) // math.gcd(text1_length, text2_length)

        while True:  # Continuous loop for scrolling
            for i in range(loop_index): 
                
                display_text1 = text1[i:] + text1[:i]

                # Get the current slice of the text to display for line 2
                display_text2 = text2[i:] + text2[:i]

                # Display the current slices on the LCD
                self.lcd.lcd_display_string(display_text1, 1)  # Display on line 1
                self.lcd.lcd_display_string(display_text2, 2)  # Display on line 2
                
                time.sleep(duration_per_shift)  # Delay for scrolling effect

# Example usage (assuming `lcd` is already defined and initialized):
# scrolling_display = ScrollingDisplay(lcd, max_width=16)
# scrolling_display.scroll_texts("Happiness", "Joyful", duration_per_shift=0.3)
