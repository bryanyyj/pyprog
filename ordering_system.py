class order:
    def __init__(self):
        # Define your menu items and prices
        self.stalls = {
            1: "Drinks",
            2: "Snacks",
            3: "Chicken Rice",
            4: "Western",
            5: "Halal"
        }

        self.menus = {
            1: {1: ("Milo", 1.50), 2: ("Juice", 1.50), 3: ("Water", 1.00)},
            2: {1: ("Luo Mi Gao", 2.00), 2: ("Cookies", 1.50), 3: ("Sandwich", 1.00)},
            3: {1: ("Chicken Rice", 5.00), 2: ("Chicken Soup", 3.50)},
            4: {1: ("Baked Rice", 5.00), 2: ("Burger", 4.00), 3: ("Fries", 2.00)},
            5: {1: ("Briyanni", 5.50), 2: ("Rendang", 4.50)}
        }


        self.order = []