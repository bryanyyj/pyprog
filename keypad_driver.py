import RPi.GPIO as GPIO
from time import sleep
from threading import Thread, Lock

class Keypad:
    def __init__(self, rows, cols, layout):
        """
        Initializes the keypad with given row pins, column pins, and key layout.

        :param rows: List of GPIO pins connected to the rows.
        :param cols: List of GPIO pins connected to the columns.
        :param layout: 2D list representing the keypad layout.
        """
        self.ROW = rows
        self.COL = cols
        self.MATRIX = layout
        self.last_key = None
        self.lock = Lock()
        self.running = True
        self.thread = Thread(target=self._scan_keypad, daemon=True)

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Configure column pins as outputs and set them high
        for col_pin in self.COL:
            GPIO.setup(col_pin, GPIO.OUT)
            GPIO.output(col_pin, 1)

        # Configure row pins as inputs with pull-up resistors
        for row_pin in self.ROW:
            GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Start the keypad scanning thread
        self.thread.start()

    def _scan_keypad(self):
        """Background thread for scanning the keypad."""
        while self.running:
            for col_index, col_pin in enumerate(self.COL):
                GPIO.output(col_pin, 0)  # Pull one column pin low
                for row_index, row_pin in enumerate(self.ROW):
                    if GPIO.input(row_pin) == 0:  # Key is pressed
                        key = self.MATRIX[row_index][col_index]
                        with self.lock:
                            self.last_key = key
                        while GPIO.input(row_pin) == 0:  # Debounce
                            sleep(0.1)
                GPIO.output(col_pin, 1)  # Reset the column pin
            sleep(0.1)  # Slight delay to reduce CPU usage

    def get_last_key(self):
        """
        Retrieves the last key pressed and clears it.

        :return: The last key pressed, or None if no key has been pressed.
        """
        with self.lock:
            key = self.last_key
            self.last_key = None
        return key

    def cleanup(self):
        """Stops the thread and cleans up the GPIO pins."""
        self.running = False
        self.thread.join()
        GPIO.cleanup()
