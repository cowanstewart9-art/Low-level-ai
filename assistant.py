import json
import os

def load_data(filename):
    """Loads data from a JSON file."""
    if not os.path.exists(filename):
        print(f"Error: Data file not found at '{filename}'")
        return None
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filename}'. File might be empty or corrupt.")
        return [] # Return empty list if file is corrupt or empty

def save_data(filename, data):
    """Saves data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def find_palmon(name, palmons):
    """Finds a Palmon by name and displays its information."""
    for palmon in palmons:
        if palmon['name'].lower() == name:
            print(f"\n--- {palmon['name']} ---")
            print(f"  Type: {palmon['type']}")
            print(f"  Abilities: {', '.join(palmon['abilities'])}")
            print(f"  Strengths: {', '.join(palmon['strengths'])}")
            print(f"  Weaknesses: {', '.join(palmon['weaknesses'])}")
            print(f"  Rarity: {palmon['rarity']}")
            return
    print(f"Palmon '{name}' not found.")

def find_crafting_recipe(item_name, crafting):
    """Finds a crafting recipe by item name and displays it."""
    for recipe in crafting:
        if recipe['item'].lower() == item_name:
            print(f"\n--- {recipe['item']} ---")
            print(f"  Description: {recipe['description']}")
            print("  Ingredients:")
            for ingredient in recipe['ingredients']:
                print(f"    - {ingredient['name']}: {ingredient['quantity']}")
            return
    print(f"Crafting recipe for '{item_name}' not found.")

def find_location(name, locations):
    """Finds a location by name and displays its information."""
    for location in locations:
        if location['name'].lower() == name:
            print(f"\n--- {location['name']} ---")
            print(f"  Description: {location['description']}")
            print(f"  Palmons: {', '.join(location['palmons'])}")
            print(f"  Resources: {', '.join(location['resources'])}")
            return
    print(f"Location '{name}' not found.")

def add_palmon(palmons):
    """Adds a new Palmon to the knowledge base."""
    try:
        name = input("Enter Palmon name: ")
        if any(p['name'].lower() == name.lower() for p in palmons):
            print("A Palmon with this name already exists.")
            return
        type = input("Enter type: ")
        abilities = input("Enter abilities (comma-separated): ").split(',')
        strengths = input("Enter strengths (comma-separated): ").split(',')
        weaknesses = input("Enter weaknesses (comma-separated): ").split(',')
        rarity = input("Enter rarity: ")

        new_palmon = {
            "name": name, "type": type,
            "abilities": [a.strip() for a in abilities],
            "strengths": [s.strip() for s in strengths],
            "weaknesses": [w.strip() for w in weaknesses],
            "rarity": rarity
        }
        palmons.append(new_palmon)
        save_data('data/palmons.json', palmons)
        print(f"Successfully added '{name}' to the knowledge base.")
    except (EOFError, KeyboardInterrupt):
        print("\nAdd operation cancelled.")


def add_recipe(crafting):
    """Adds a new crafting recipe to the knowledge base."""
    try:
        item = input("Enter item name: ")
        if any(r['item'].lower() == item.lower() for r in crafting):
            print("A recipe for this item already exists.")
            return
        description = input("Enter description: ")
        ingredients = []
        while True:
            ingredient_name = input("Enter ingredient name (or 'done'): ")
            if ingredient_name.lower() == 'done':
                break
            try:
                quantity = int(input(f"Enter quantity for {ingredient_name}: "))
                ingredients.append({"name": ingredient_name, "quantity": quantity})
            except ValueError:
                print("Invalid quantity. Please enter a number.")

        new_recipe = {"item": item, "description": description, "ingredients": ingredients}
        crafting.append(new_recipe)
        save_data('data/crafting.json', crafting)
        print(f"Successfully added recipe for '{item}' to the knowledge base.")
    except (EOFError, KeyboardInterrupt):
        print("\nAdd operation cancelled.")

def add_location(locations):
    """Adds a new location to the knowledge base."""
    try:
        name = input("Enter location name: ")
        if any(l['name'].lower() == name.lower() for l in locations):
            print("A location with this name already exists.")
            return
        description = input("Enter description: ")
        palmons = input("Enter Palmons found (comma-separated): ").split(',')
        resources = input("Enter resources found (comma-separated): ").split(',')

        new_location = {
            "name": name,
            "description": description,
            "palmons": [p.strip() for p in palmons],
            "resources": [r.strip() for r in resources]
        }
        locations.append(new_location)
        save_data('data/locations.json', locations)
        print(f"Successfully added '{name}' to the knowledge base.")
    except (EOFError, KeyboardInterrupt):
        print("\nAdd operation cancelled.")


def main():
    """Main function to run the Palmon Survival AI assistant."""
    print("Welcome to the Palmon Survival AI Assistant!")
    print("Type 'help' to see a list of available commands.")

    palmons = load_data('data/palmons.json')
    crafting = load_data('data/crafting.json')
    locations = load_data('data/locations.json')

    if palmons is None or crafting is None or locations is None:
        print("Could not load all data files. Exiting.")
        return

    while True:
        try:
            command_line = input("> ").strip().lower()
            if not command_line:
                continue

            parts = command_line.split()
            command = parts[0]
            args = ' '.join(parts[1:])

            if command == "exit":
                print("Goodbye!")
                break
            elif command == "help":
                print("\nAvailable Commands:")
                print("  help - Show this help message")
                print("  exit - Exit the assistant")
                print("  palmon <name> - Get information about a specific Palmon")
                print("  craft <item> - Get the crafting recipe for an item")
                print("  location <name> - Get information about a location")
                print("  add palmon - Add a new Palmon to the knowledge base")
                print("  add recipe - Add a new crafting recipe")
                print("  add location - Add a new location")
            elif command == "palmon":
                if args: find_palmon(args, palmons)
                else: print("Please specify a Palmon name.")
            elif command == "craft":
                if args: find_crafting_recipe(args, crafting)
                else: print("Please specify an item name.")
            elif command == "location":
                if args: find_location(args, locations)
                else: print("Please specify a location name.")
            elif command == "add":
                if args == "palmon":
                    add_palmon(palmons)
                elif args == "recipe":
                    add_recipe(crafting)
                elif args == "location":
                    add_location(locations)
                else:
                    print("You can add a 'palmon', 'recipe', or 'location'.")
            else:
                print(f"Unknown command: '{command}'")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()
