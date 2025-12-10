from palmon_assistant.core import PalmonAssistant


def show_help():
    """Displays the help message."""
    print("\nAvailable Commands:")
    print("  help - Show this help message")
    print("  exit - Exit the assistant")
    print("  palmon <name> - Get information about a specific Palmon")
    print("  craft <item> - Get the crafting recipe for an item")
    print("  location <name> - Get information about a location")
    print("  add palmon - Add a new Palmon to the knowledge base")
    print("  add recipe - Add a new crafting recipe")
    print("  add location - Add a new location")


def handle_add_palmon(assistant):
    """Handles adding a new Palmon."""
    try:
        name = input("Enter Palmon name: ")
        palmon_type = input("Enter type: ")
        abilities = input("Enter abilities (comma-separated): ").split(',')
        strengths = input("Enter strengths (comma-separated): ").split(',')
        weaknesses = input("Enter weaknesses (comma-separated): ").split(',')
        rarity = input("Enter rarity: ")

        palmon_data = {
            "name": name,
            "type": palmon_type,
            "abilities": [a.strip() for a in abilities],
            "strengths": [s.strip() for s in strengths],
            "weaknesses": [w.strip() for w in weaknesses],
            "rarity": rarity
        }
        result = assistant.add_palmon(palmon_data)
        print(result)
    except (EOFError, KeyboardInterrupt):
        print("\nAdd operation cancelled.")


def handle_add_recipe(assistant):
    """Handles adding a new crafting recipe."""
    try:
        item = input("Enter item name: ")
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
        recipe_data = {"item": item, "description": description, "ingredients": ingredients}
        result = assistant.add_recipe(recipe_data)
        print(result)
    except (EOFError, KeyboardInterrupt):
        print("\nAdd operation cancelled.")


def handle_add_location(assistant):
    """Handles adding a new location."""
    try:
        name = input("Enter location name: ")
        description = input("Enter description: ")
        palmons = input("Enter Palmons found (comma-separated): ").split(',')
        resources = input("Enter resources found (comma-separated): ").split(',')
        location_data = {
            "name": name,
            "description": description,
            "palmons": [p.strip() for p in palmons],
            "resources": [r.strip() for r in resources]
        }
        result = assistant.add_location(location_data)
        print(result)
    except (EOFError, KeyboardInterrupt):
        print("\nAdd operation cancelled.")


def main():
    """Main function to run the Palmon Survival AI assistant."""
    assistant = PalmonAssistant()

    print("Welcome to the Palmon Survival AI Assistant!")
    print("Type 'help' to see a list of available commands.")

    if not assistant.palmons or not assistant.crafting or not assistant.locations:
        print("Warning: Some data files could not be loaded. "
              "The assistant may not function as expected.")

    while True:
        try:
            command_line = input("> ").strip().lower()
            if not command_line:
                continue

            parts = command_line.split()
            command = parts[0]
            args = ' '.join(parts[1:])

            if len(args) > 1 and ((args.startswith("'") and args.endswith("'")) or
                                  (args.startswith('"') and args.endswith('"'))):
                args = args[1:-1]

            if command == "exit":
                print("Goodbye!")
                break
            elif command == "help":
                show_help()
            elif command == "palmon":
                if args:
                    palmon = assistant.find_palmon(args)
                    if palmon:
                        print(f"\n--- {palmon['name']} ---")
                        print(f"  Type: {palmon['type']}")
                        print(f"  Abilities: {', '.join(palmon['abilities'])}")
                        print(f"  Strengths: {', '.join(palmon['strengths'])}")
                        print(f"  Weaknesses: {', '.join(palmon['weaknesses'])}")
                        print(f"  Rarity: {palmon['rarity']}")
                    else:
                        print(f"Palmon '{args}' not found.")
                else:
                    print("Please specify a Palmon name.")
            elif command == "craft":
                if args:
                    recipe = assistant.find_crafting_recipe(args)
                    if recipe:
                        print(f"\n--- {recipe['item']} ---")
                        print(f"  Description: {recipe['description']}")
                        print("  Ingredients:")
                        for ingredient in recipe['ingredients']:
                            print(f"    - {ingredient['name']}: {ingredient['quantity']}")
                    else:
                        print(f"Crafting recipe for '{args}' not found.")
                else:
                    print("Please specify an item name.")
            elif command == "location":
                if args:
                    location = assistant.find_location(args)
                    if location:
                        print(f"\n--- {location['name']} ---")
                        print(f"  Description: {location['description']}")
                        print(f"  Palmons: {', '.join(location['palmons'])}")
                        print(f"  Resources: {', '.join(location['resources'])}")
                    else:
                        print(f"Location '{args}' not found.")
                else:
                    print("Please specify a location name.")
            elif command == "add":
                if args == "palmon":
                    handle_add_palmon(assistant)
                elif args == "recipe":
                    handle_add_recipe(assistant)
                elif args == "location":
                    handle_add_location(assistant)
                else:
                    print("You can add a 'palmon', 'recipe', or 'location'.")
            else:
                print(f"Unknown command: '{command}'")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
