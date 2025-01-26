import time

class ScrollingDisplay:
    def __init__(self, lcd, max_width):
        self.lcd = lcd
        self.max_width = max_width

    def scroll_texts(self, text1, text2, duration_per_shift=0.3):
        # Create padded versions of the texts
        text1 = text1 + " "  # Add space at the end for separation
        text2 = text2 + " "  # Add space at the end for separation
        text1_length = len(text1)
        text2_length = len(text2)

        # Calculate total length for scrolling
        max_length = max(text1_length, text2_length) + self.max_width

        while True:  # Continuous loop for scrolling
            for i in range(max_length):  # Loop through max_length
                # Get the current slice of the text to display for line 1
                if i < text1_length:
                    display_text1 = text1[i:i + self.max_width].ljust(self.max_width, '_')
                else:
                    display_text1 = '_' * self.max_width  # Fill with underscores if out of range

                # Get the current slice of the text to display for line 2
                if i < text2_length:
                    display_text2 = text2[i:i + self.max_width].ljust(self.max_width, '_')
                else:
                    display_text2 = '_' * self.max_width  # Fill with underscores if out of range

                # Display the current slices on the LCD
                self.lcd.lcd_display_string(display_text1, 1)  # Display on line 1
                self.lcd.lcd_display_string(display_text2, 2)  # Display on line 2
                
                time.sleep(duration_per_shift)  # Delay for scrolling effect

# Example usage (assuming `lcd` is already defined and initialized):
# scrolling_display = ScrollingDisplay(lcd, max_width=16)
# scrolling_display.scroll_texts("Happiness", "Joyful", duration_per_shift=0.3)
