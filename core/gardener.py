import time as t

class Gardener:
    def __init__(self, actions, images, orders, navigator):
        self.actions = actions
        self.Images = images
        self.Orders = orders
        self.navigator = navigator

    def garden(self, spell_order, garden):
        # Go to the garden
        print(f"Navigating to garden...")
        self.navigator.navigate_to_location(garden)

        # Handle plant needs
        if self.actions.is_image_visible(self.Images.HAS_NEEDS):
            self.handle_needs(spell_order)

        # If plants are ready to harvest, harvest them
        if self.actions.is_image_visible(self.Images.HARVEST):
            is_elder = self.harvest()

            if is_elder:
                self.replant_seeds(garden)

        self.replant_seeds(garden)

    def handle_needs(self, spell_order):
        for entry in spell_order:
            spell = entry.get("spell")
            coordinates = entry.get("coordinates")
            spell_image = getattr(self.Images, spell, None)

            self.actions.press_key("g")
            t.sleep(1)

            if not spell_image:
                print(f"Spell image for {spell} not found.")
                continue

            print(f"Looking for spell: {spell}...")
            while not self.actions.is_image_visible(spell_image):
                print(f"{spell} not found on screen. Clicking arrow button...")
                if not self.actions.click_image(self.Images.GARDENING_RIGHT_ARROW):
                    print("Failed to locate the arrow button.")
                    return
                t.sleep(0.5)

            print(f"{spell} found. Selecting spell...")
            if self.actions.click_image(spell_image):
                print(f"{spell} selected. Casting spell...")
                if coordinates:
                    self.actions.move_mouse_to(*coordinates, duration=0.5)
                    t.sleep(1)
                    self.actions.click() 
                    t.sleep(1000)
                else:
                    print(f"No coordinates specified for {spell}.")
                t.sleep(3)
            else:
                print(f"Failed to select {spell}.")

            self.actions.press_key("g")

    def harvest(self):
        is_elder = self.actions.is_image_visible(self.Images.ELDER)
        if is_elder:
            print("Crops are Elder!")
        print("Starting the harvesting process...")

        # Jump to remove obstacles and close the gardening menu
        self.actions.press_key(" ")

        # Move forward and face right
        self.actions.press_key("w", 0.2)
        self.actions.press_key("d", 0.5)
        
        # Move in a circle while spamming 'x'
        total_x_presses = 0
        self.actions.hold_key("w")
        self.actions.hold_key("a")
        try:
            while total_x_presses < 69:
                self.actions.press_key("x")
                total_x_presses += 1
                print(f"Pressed 'x' {total_x_presses} times.")
                t.sleep(0.2)
        finally:
            self.actions.release_key("w")
            self.actions.release_key("a")

        print("Harvesting process completed.")

        # Reset housing items
        self.actions.press_key("h")
        self.actions.press_key("h")
        return is_elder
    
    def replant_seeds(self, garden):
        print("Replanting seeds...")

        # Navigate back to the garden and open the gardening menu
        self.navigator.go_to_start_of_house()
        self.navigator.navigate_to_location(garden)
        self.actions.press_key("g")

        # Plant the first seed
        self.actions.click_image(self.Images.SEEDS)
        self.actions.click_image(self.Images.COUCH_POTATOES)
        self.actions.move_mouse_to(1664, 618)
        self.actions.click()
        t.sleep(6)

        # Plant all seeds
        self.actions.click_image(self.Images.UTILITY_SPELLS)
        self.actions.click_image(self.Images.PLANT_ALL)
        self.actions.move_mouse_to(1712, 616)
        self.actions.click()
        self.actions.click_image(self.Images.YES)