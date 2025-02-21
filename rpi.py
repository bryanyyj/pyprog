import csv
import I2C_LCD_driver
import datetime
import menu
import scrolling_display

import app

lcd = I2C_LCD_driver.lcd()
lcd.lcd_clear()

ROW_PINS = [5, 6, 13, 19]
COL_PINS = [12, 16, 20, 21]
KEYPAD_LAYOUT = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

lcd_keypad = scrolling_display.LCDKeypad(ROW_PINS, COL_PINS, KEYPAD_LAYOUT)

def get_order_from_stall(stall_no):
    """Handles ordering from a specific stall."""
    total_order, total_price = "", 0
    stall = menu.stalls[stall_no]
    
    while True:
        stall_foods = " | ".join(f"{i+1}. {food} ${price:.2f}" for i, (food, price) in enumerate(stall.items()))
        order_food = lcd_keypad.scroll_texts_for_keypress("Choose an item to order", stall_foods)
        
        quantity = int(lcd_keypad.scroll_texts_for_keypress("How many?", f"Order for {order_food} - {stall[order_food]:.2f}"))
        total_order += f"{order_food} x{quantity}, "
        total_price += stall[order_food] * quantity
        
        if lcd_keypad.scroll_texts_for_keypress("Order more from this stall?", "* - Yes | # - No") == "#":
            break
    
    return total_order.strip(", "), total_price

def save_order(orders):
    """Saves the order details to separate CSV files per stall."""
    for stall_no, (total_order, total_price) in orders.items():
        with open(f"stall{stall_no}.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([stall_no, total_order, total_price, datetime.datetime.now(), 0])

def main():
    orders = {}
    while True:
        stall = menu.stalls
        stall_no = lcd_keypad.scroll_texts_for_keypress(
            "Welcome! Choose a stall from 1 to 5",
            " | ".join(f"{i+1}- {stall[i+1]}" for i in range(5))
        )
        
        total_order, total_price = get_order_from_stall(stall_no)
        orders[stall_no] = (total_order, total_price)
        
        while lcd_keypad.scroll_texts_for_keypress("Order from another stall?", "* - Yes | # - No") == "*":
            stall_no = lcd_keypad.scroll_texts_for_keypress(
                "Choose another stall",
                " | ".join(f"{i+1}- {stall[i+1]}" for i in range(5))
            )
            extra_order, extra_price = get_order_from_stall(stall_no)
            if stall_no in orders:
                orders[stall_no] = (orders[stall_no][0] + f", {extra_order}", orders[stall_no][1] + extra_price)
            else:
                orders[stall_no] = (extra_order, extra_price)
        
        if lcd_keypad.scroll_texts_for_keypress("End ordering?", "* - Yes | # - No") == "*":
            save_order(orders)
            break
        
if __name__ == "__main__":
    main()
