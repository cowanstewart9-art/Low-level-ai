import json
import os


class PalmonAssistant:
    def __init__(self, data_path=None):
        if data_path is None:
            # Get the directory of the current script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.data_path = os.path.join(base_dir, '..', 'data')
        else:
            self.data_path = data_path

        self.world_data = self.load_world_data()
        self.palmons = self.world_data.get('palmons', [])
        self.crafting = self.world_data.get('crafting', [])
        self.locations = self.world_data.get('locations', [])

    def load_world_data(self):
        """Loads all data from the palmon_world.json file."""
        filepath = os.path.join(self.data_path, 'palmon_world.json')
        if not os.path.exists(filepath):
            return {}
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def save_world_data(self):
        """Saves all data to the palmon_world.json file."""
        filepath = os.path.join(self.data_path, 'palmon_world.json')
        with open(filepath, 'w') as f:
            json.dump(self.world_data, f, indent=2)

    def find_palmon(self, name):
        """Finds a Palmon by name and returns its information."""
        name = name.lower()
        for palmon in self.palmons:
            if palmon['name'].lower() == name:
                return palmon
        return None

    def find_crafting_recipe(self, item_name):
        """Finds a crafting recipe by item name and returns it."""
        item_name = item_name.lower()
        for recipe in self.crafting:
            if recipe['item'].lower() == item_name:
                return recipe
        return None

    def find_location(self, name):
        """Finds a location by name and returns its information."""
        name = name.lower()
        for location in self.locations:
            if location['name'].lower() == name:
                return location
        return None

    def add_palmon(self, palmon_data):
        """Adds a new Palmon to the knowledge base."""
        name = palmon_data.get('name', '').lower()
        if any(p['name'].lower() == name for p in self.palmons):
            return "A Palmon with this name already exists."
        self.palmons.append(palmon_data)
        self.save_world_data()
        return f"Successfully added '{palmon_data['name']}' to the knowledge base."

    def add_recipe(self, recipe_data):
        """Adds a new crafting recipe to the knowledge base."""
        item = recipe_data.get('item', '').lower()
        if any(r['item'].lower() == item for r in self.crafting):
            return "A recipe for this item already exists."
        self.crafting.append(recipe_data)
        self.save_world_data()
        return f"Successfully added recipe for '{recipe_data['item']}' to the knowledge base."

    def add_location(self, location_data):
        """Adds a new location to the knowledge base."""
        name = location_data.get('name', '').lower()
        if any(loc['name'].lower() == name for loc in self.locations):
            return "A location with this name already exists."
        self.locations.append(location_data)
        self.save_world_data()
        return f"Successfully added '{location_data['name']}' to the knowledge base."
