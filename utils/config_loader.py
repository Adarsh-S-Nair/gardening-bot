import json

class ConfigLoader:
    class IMAGES:
        pass

    class LOCATIONS:
        pass

    class ORDERS:
        pass

    @staticmethod
    def load_config(
        image_file="./config/images.json",
        movement_file="./config/movements.json",
        order_file="./config/orderings.json"
    ):
        try:
            # Load image paths
            with open(image_file, "r") as f:
                config_data = json.load(f)
            for key, value in config_data.items():
                setattr(ConfigLoader.IMAGES, key, value)

            # Load movement sequences
            with open(movement_file, "r") as f:
                movement_data = json.load(f)
            for key, value in movement_data.items():
                setattr(ConfigLoader.LOCATIONS, key, value)

            # Load gardening orders
            with open(order_file, "r") as f:
                order_data = json.load(f)
            for key, value in order_data.items():
                setattr(ConfigLoader.ORDERS, key, value)

        except Exception as e:
            print(f"Error loading config files: {e}")
            raise e
