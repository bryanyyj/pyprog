import time
import csv
import I2C_LCD_driver
import datetime
import menu
import scrolling_display
import stall1_tel
import os
import json
import threading
from webapp import app  

lcd = I2C_LCD_driver.lcd()
lcd.lcd_clear()
order_id = 0
MATRIX = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9],
          ['*', 0, '#']]  # layout of keys on keypad
ROW = [6, 20, 19, 13]  # row pins
COL = [12, 5, 16]  # column pins

lcd_keypad = scrolling_display.LCDKeypad(ROW, COL, MATRIX)
JSON_FILE = "display.json"

def get_order_from_stall(stall_no):
    """Handles ordering from a specific stall."""
    total_order, total_price = "", 0
    stall_menu = menu.menus[stall_no]  # Get the menu for the selected stall

    while True:
        # Display available food items with prices
        stall_foods = " | ".join(f"{key}. {food} ${price:.2f}" for key, (food, price) in stall_menu.items())
        
        # Get user selection
        order_key = int(lcd_keypad.scroll_texts_for_keypress("Choose an item to order", stall_foods))
        
        # Ensure the selection is valid
        if order_key not in stall_menu:
            lcd_keypad.scroll_texts_for_keypress("Invalid choice!", "Press any key to retry")
            continue
        
        order_food, food_price = stall_menu[order_key]

        # Ask for quantity
        quantity = int(lcd_keypad.scroll_texts_for_keypress("How many?", f"Order for {order_food} - ${food_price:.2f}"))
        
        # Update total order and price
        total_order += f"{order_food} x{quantity}, "
        total_price += food_price * quantity
        
        # Check if the user wants to order more
        if lcd_keypad.scroll_texts_for_keypress("Order more from this stall?", "* - Yes | # - No") == "#":
            break
    
    return total_order.strip(", "), total_price

def save_order(orders, filename='display.json'):
    """Saves the order details to a JSON file."""
    global order_id  # Declare order_id as global
    temp_list = []

    # Initialize or read existing JSON data
    if os.path.exists(filename):
        with open(filename, 'r') as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                data = {"orders": []}  # Create a new dictionary if the file is empty
    else:
        data = {"orders": []}  # Create a new dictionary if the file doesn't exist

    for stall_no, (total_order, total_price) in orders.items():
        order_id += 1
        if stall_no == 1:
            stall1_tel.send_order_to_stall(f"{total_order} - Total: ${total_price:.2f}", order_id)

        temp_list.append(order_id)

        # Write order details to the stall's CSV file
        with open(f"stall{stall_no}.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([order_id, total_order, total_price, datetime.datetime.now(), 0])

        # Append the order_id to the JSON data
        data["orders"].append(order_id)

    # Write the updated JSON data back to the file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return temp_list

def order_process():
    global order_id
    orders = {}  # Stores all orders from different stalls

    while True:
        # Display stall selection
        stall_no = int(lcd_keypad.scroll_texts_for_keypress(
            "Welcome! Choose a stall from 1 to 5",
            " | ".join(f"{i}- {menu.stalls[i]}" for i in menu.stalls)
        ))

        # Ensure the selection is valid
        if stall_no not in menu.stalls:
            lcd_keypad.scroll_texts_for_keypress("Invalid choice!", "Press any key to retry")
            continue

        # Get order details from the selected stall
        total_order, total_price = get_order_from_stall(stall_no)

        # Store or append to existing orders
        if stall_no in orders:
            orders[stall_no] = (
                orders[stall_no][0] + f", {total_order}",
                orders[stall_no][1] + total_price
            )
        else:
            orders[stall_no] = (total_order, total_price)

        # Ask if the user wants to order from another stall
        while lcd_keypad.scroll_texts_for_keypress("Order from another stall?", "* - Yes | # - No") == "*":
            stall_no = int(lcd_keypad.scroll_texts_for_keypress(
                "Choose another stall",
                " | ".join(f"{i}- {menu.stalls[i]}" for i in menu.stalls)
            ))

            if stall_no not in menu.stalls:
                lcd_keypad.scroll_texts_for_keypress("Invalid choice!", "Press any key to retry")
                continue

            extra_order, extra_price = get_order_from_stall(stall_no)

            if stall_no in orders:
                orders[stall_no] = (
                    orders[stall_no][0] + f", {extra_order}",
                    orders[stall_no][1] + extra_price
                )
            else:
                orders[stall_no] = (extra_order, extra_price)

        # Ask if the user wants to finalize the order or continue
        if lcd_keypad.scroll_texts_for_keypress("Finalize order?", "* - Yes | # - No") == "*":
            save_order(orders)

            order_summary = ", ".join(f"{key}: {value[0]} (${value[1]:.2f})" for key, value in orders.items())
            lcd_keypad.scroll_texts_for_keypress(f"Your ID is -> {order_id}", order_summary)
            orders.clear()  # Clear orders for the next round
        else:
            lcd_keypad.scroll_texts_for_keypress("Continue ordering...", "Press any key to continue")

if __name__ == '__main__':
    # Start the order processing in a separate thread
    threading.Thread(target=order_process, daemon=True).start()
    time.sleep(60)
    # Run the Flask web application
    app.run(debug=True, threaded=True)
