import time
import csv
import I2C_LCD_driver as lcd
import keypad_driver
import math
import datetime
import menu
import scrolling_display
lcd = I2C_LCD_driver.lcd()
lcd.lcd_clear()


while True:
    total_order = ""
    total_price = ""
    order_done = False
    #choose which stall
    if order_done == False
        stall = menu.stalls
        stall_no = scrolling_display.scroll_texts_for_keypress("Welcome! Choose a stall from 1 to 5",f"1- {stall[1]} 2- {stall[1]} 3- {stall[1]} 4- {stall[1]} 5- {stall[1]}")
        stall_order = stall_no
        order_food = scrolling_display.scroll_texts_for_keypress("Choose an item to order"," | ".join(f"{i+1}. {food} ${price:.2f}" for i, (food, price) in enumerate(stall[stall_no].values())))

        quantity = scrolling_display.scroll_texts_for_keypress("how many?", f"order for {stall[stall_no][order_food][0]} - {stall[stall_no][order_food][1]:2f}")

        total_order += stall[stall_no][order_food][0]
        total_price += (stall[stall_no][order_food][1] * quantity)

        same_stall = scrolling_display.scroll_texts_for_keypress("Do you want to order from the same stall?","A - yes | B - no")
        if same_stall == "A":
            order_food = scrolling_display.scroll_texts_for_keypress("Choose an item to order"," | ".join(f"{i+1}. {food} ${price:.2f}" for i, (food, price) in enumerate(stall[stall_no].values())))
            quantity = scrolling_display.scroll_texts_for_keypress("how many?", f"order for {stall[stall_no][order_food][0]} - {stall[stall_no][order_food][1]:2f}")
            total_order += stall[stall_no][order_food][0]
            total_price += (stall[stall_no][order_food][1] * quantity)
            same_stall = scrolling_display.scroll_texts_for_keypress("Do you want to order from the same stall?","A - yes | B - no")
        else:
            check = scrolling_display.scroll_texts_for_keypress("Do you want to order from another stall?","A - yes | B - no")
            if check == "B":
                end_order = scrolling_display.scroll_texts_for_keypress("Do you want to end ordering?","A - yes | B - no")
                if end_order == "A":
                    order_done = True
                    data_row = [stall_no, total_order, total_price, datetime.now()]
                    with open(f"stall{stall_no}.csv", mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(data_row) 
            else:
                data_row = [stall_no, total_order, total_price, datetime.now()]
                with open(f"stall{stall_no}.csv", mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(data_row) 