import time as t

class Gardener:
    def __init__(self, actions, images, orders, locations, navigator):
        self.actions = actions
        self.Images = images
        self.Orders = orders
        self.Locations = locations
        self.navigator = navigator

    def garden(self, spell_order, garden):
        # Go to the garden
        print(f"Navigating to garden...")
        self.navigator.navigate_to_location(garden)

        # Handle plant needs
        if self.actions.is_image_visible(self.Images.HAS_NEEDS):
            print("Plants have needs! Handling needs...")
            self.cast_spell_order(spell_order)

        # If plants are ready to harvest, harvest them
        if self.actions.is_image_visible(self.Images.HARVEST):
            is_elder = self.harvest()

            if is_elder:
                print("Plants were elder! Replanting seeds...")
                self.replant_seeds(garden)

    def cast_spell_order(self, spell_order):
        self.actions.press_key("g")
        
        for step in spell_order:
            spell = step.get("spell")
            coordinates = step.get("coordinates")
            category = step.get("category")
            if not self.find_spell(spell, category):
                print(f"Failed to find spell: {spell}")
                return
            
            if not self.cast_spell(spell, coordinates):
                print(f"Failed to cast spell: {spell}")
                return
        
        self.actions.press_key("g")

    def find_spell(self, spell, category):
        category_image = getattr(self.Images, category, None)
        spell_image = getattr(self.Images, spell, None)
        
        print(f"Navigating to category: {category}...")
        if not self.actions.click_image(category_image):
            print(f"Failed to locate category: {category}.")
            return False
        
        print(f"Looking for spell: {spell}...")
        while not self.actions.is_image_visible(spell_image):
            print(f"{spell} not found on screen. Clicking arrow button...")
            if not self.actions.click_image(self.Images.GARDENING_RIGHT_ARROW):
                print("Failed to locate the arrow button.")
                return False
            t.sleep(0.5)
        
        print(f"Spell {spell} found")
        return True
    
    def cast_spell(self, spell, coordinates):
        spell_image = getattr(self.Images, spell, None)
        if not self.actions.click_image(spell_image):
            print(f"Failed to select spell: {spell}.")
            return False
        
        print(f"Spell {spell} selected. Casting spell...")
        if coordinates:
            self.actions.move_mouse_to(*coordinates, duration=0.5)
            t.sleep(5)
            self.actions.click()
        else:
            print(f"No coordinates specified for {spell}.")
        t.sleep(10)
        return True

    def harvest(self):
        print("Starting the harvesting process...")
        is_elder = self.actions.is_image_visible(self.Images.ELDER)
        self.navigator.navigate_to_location(self.Locations.HARVEST_SPOT)
        self.actions.hold_key("w")
        self.actions.hold_key("a")

        harvest_absent_start = None
        try:
            while True:
                self.actions.press_key("x")
                t.sleep(0.1)

                if not self.actions.is_image_visible(self.Images.HARVEST):
                    harvest_absent_start = harvest_absent_start or t.time()
                    if t.time() - harvest_absent_start > 5:
                        break
                else:
                    harvest_absent_start = None
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

        # Plant the first seed
        self.cast_spell_order(self.Orders.PLANT_ALL)
        self.actions.click_image(self.Images.YES)