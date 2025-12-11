import json
import os
import shutil

GAMES_DIR = "data/games"


class Game:
    def __init__(self, name):
        self.name = name
        self.path = os.path.join(GAMES_DIR, name)
        self.structure_file = os.path.join(self.path, "structure.json")
        self.structure = self._load_structure()
        self.data = {}
        self._load_data()

    def _load_structure(self):
        if os.path.exists(self.structure_file):
            try:
                with open(self.structure_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error: Could not decode structure for game "
                      f"'{self.name}'.")
                return {"categories": {}}
        return {"categories": {}}

    def _save_structure(self):
        with open(self.structure_file, 'w') as f:
            json.dump(self.structure, f, indent=2)

    def _load_data(self):
        # Check storage mode
        storage_mode = self.structure.get("storage_mode", "multiple_files")

        if storage_mode == "single_file":
            data_file = self.structure.get("data_file", f"{self.name}.json")
            file_path = os.path.join(self.path, data_file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        self.data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Error: Could not decode data file '{data_file}'.")
                    self.data = {}
            else:
                self.data = {}

            # Ensure all categories exist in data
            for category in self.structure.get("categories", {}):
                if category not in self.data:
                    self.data[category] = []
        else:
            # Multiple files mode (legacy/default)
            for category, config in self.structure.get("categories", {}).items():
                file_path = os.path.join(self.path, config.get("file", f"{category}.json"))
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'r') as f:
                            self.data[category] = json.load(f)
                    except json.JSONDecodeError:
                        print(f"Error: Could not decode data for category "
                              f"'{category}'.")
                        self.data[category] = []
                else:
                    self.data[category] = []

    def save_data(self, category=None):
        storage_mode = self.structure.get("storage_mode", "multiple_files")

        if storage_mode == "single_file":
            data_file = self.structure.get("data_file", f"{self.name}.json")
            file_path = os.path.join(self.path, data_file)
            with open(file_path, 'w') as f:
                json.dump(self.data, f, indent=2)
        else:
            if category and category in self.structure.get("categories", {}):
                config = self.structure["categories"][category]
                file_path = os.path.join(self.path, config.get("file", f"{category}.json"))
                with open(file_path, 'w') as f:
                    json.dump(self.data[category], f, indent=2)

    def find_entry(self, category, search_term):
        if category not in self.data:
            print(f"Category '{category}' does not exist.")
            return

        entries = self.data[category]
        key_field = self.structure["categories"][category]["key_field"]
        fields = self.structure["categories"][category]["fields"]

        found = False
        for entry in entries:
            if entry.get(key_field, "").lower() == search_term.lower():
                print(f"\n--- {entry.get(key_field)} ---")
                for field in fields:
                    val = entry.get(field)
                    if isinstance(val, list):
                        # Simple heuristic for list of objects vs list of strings
                        if val and isinstance(val[0], dict):
                            print(f"  {field.capitalize()}:")
                            for item in val:
                                # Generic printer for dict items
                                parts = [f"{k}: {v}" for k, v in item.items()]
                                print(f"    - {', '.join(parts)}")
                        else:
                            s = ', '.join(map(str, val))
                            print(f"  {field.capitalize()}: {s}")
                    else:
                        print(f"  {field.capitalize()}: {val}")
                found = True
                return

        if not found:
            print(f"Entry '{search_term}' not found in category '{category}'.")

    def add_entry(self, category):
        if category not in self.structure["categories"]:
            print(f"Category '{category}' does not exist.")
            return

        config = self.structure["categories"][category]
        key_field = config["key_field"]
        fields = config["fields"]
        entries = self.data[category]

        try:
            key_value = input(f"Enter {key_field}: ").strip()
            if any(e.get(key_field, "").lower() == key_value.lower()
                   for e in entries):
                print(f"An entry with {key_field} '{key_value}' "
                      "already exists.")
                return

            new_entry = {key_field: key_value}

            for field in fields:
                val = input(f"Enter {field}: ").strip()
                if "," in val:  # Assume list
                    val = [v.strip() for v in val.split(",")]
                elif val.isdigit():
                    val = int(val)
                new_entry[field] = val

            entries.append(new_entry)
            self.save_data(category)
            print(f"Successfully added '{key_value}' to category "
                  f"'{category}'.")

        except (EOFError, KeyboardInterrupt):
            print("\nAdd operation cancelled.")

    def create_category(self):
        try:
            name = input("Enter new category name: ").strip().lower()
            if name in self.structure["categories"]:
                print("Category already exists.")
                return

            key_field = input("Enter key field name (e.g., name, item): "
                              ).strip()
            fields_str = input("Enter other fields (comma-separated): "
                               ).strip()
            fields = [f.strip() for f in fields_str.split(",")]

            self.structure["categories"][name] = {
                "key_field": key_field,
                "fields": fields
            }
            # Add file attribute only if in multiple_files mode
            if self.structure.get("storage_mode") != "single_file":
                self.structure["categories"][name]["file"] = f"{name}.json"

            self._save_structure()

            if name not in self.data:
                self.data[name] = []

            self.save_data(name)
            print(f"Category '{name}' created.")

        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")


class GameManager:
    def __init__(self):
        self.current_game = None
        self._ensure_games_dir()

    def _ensure_games_dir(self):
        if not os.path.exists(GAMES_DIR):
            os.makedirs(GAMES_DIR)

    def list_games(self):
        if not os.path.exists(GAMES_DIR):
            return []
        return [d for d in os.listdir(GAMES_DIR)
                if os.path.isdir(os.path.join(GAMES_DIR, d))]

    def create_game(self, name):
        path = os.path.join(GAMES_DIR, name)
        if os.path.exists(path):
            print(f"Game '{name}' already exists.")
            return
        os.makedirs(path)

        # Default to single_file for new games as per latest requirement?
        # Or keep structure generic. Let's default to single_file now.
        structure = {
            "storage_mode": "single_file",
            "data_file": f"{name}.json",
            "categories": {}
        }

        with open(os.path.join(path, "structure.json"), 'w') as f:
            json.dump(structure, f, indent=2)
        print(f"Game '{name}' created.")
        self.load_game(name)

    def load_game(self, name):
        path = os.path.join(GAMES_DIR, name)
        if not os.path.exists(path):
            print(f"Game '{name}' does not exist.")
            return
        self.current_game = Game(name)
        print(f"Switched to game: {name}")

    def export_data(self, target_path, game_name=None):
        """Exports game data to a target directory."""
        if game_name:
            source_dir = os.path.join(GAMES_DIR, game_name)
            if not os.path.exists(source_dir):
                print(f"Game '{game_name}' not found.")
                return
            dest_dir = os.path.join(target_path, game_name)
        else:
            source_dir = GAMES_DIR
            dest_dir = target_path

        try:
            if os.path.exists(dest_dir):
                print(f"Warning: Destination '{dest_dir}' already exists.")
                # Auto-overwrite for Android export convenience?
                # Or keep asking? The user said "save and set aside".
                # If non-interactive pipe, input() fails.
                # Let's check if we are in a TTY.
                if sys.stdin.isatty():
                    confirm = input("Overwrite? (y/n): ").lower()
                    if confirm != 'y':
                        print("Export cancelled.")
                        return
                shutil.rmtree(dest_dir)

            shutil.copytree(source_dir, dest_dir)
            print(f"Successfully exported data to '{dest_dir}'.")
        except Exception as e:
            print(f"Export failed: {e}")


def main():
    print("Welcome to the Universal Game Assistant!")
    print("Type 'help' to see available commands.")

    manager = GameManager()

    # Auto-load Palmon Survival if it exists and is the only one
    games = manager.list_games()
    if "Palmon Survival" in games:
        manager.load_game("Palmon Survival")
    elif len(games) == 1:
        manager.load_game(games[0])

    while True:
        try:
            prompt = "> "
            if manager.current_game:
                prompt = f"{manager.current_game.name}> "

            command_line = input(prompt).strip()
            if not command_line:
                continue

            # Handle quoted arguments
            parts = []
            current_part = []
            in_quote = False
            for char in command_line:
                if char == '"' or char == "'":
                    in_quote = not in_quote
                elif char == ' ' and not in_quote:
                    if current_part:
                        parts.append(''.join(current_part))
                        current_part = []
                else:
                    current_part.append(char)
            if current_part:
                parts.append(''.join(current_part))

            if not parts:
                continue

            command = parts[0].lower()
            args = parts[1:]

            if command == "exit":
                print("Goodbye!")
                break
            elif command == "help":
                print("\nGlobal Commands:")
                print("  games - List all games")
                print("  create game <name> - Create a new game")
                print("  use <game> - Switch to a game")
                print("  export <path> - Export all data to path")
                print("  exit - Exit")

                if manager.current_game:
                    print(f"\nCommands for {manager.current_game.name}:")
                    print("  add category - Define a new category of "
                          "information")
                    print("  export game <path> - Export this game's data")
                    for cat in manager.current_game.structure["categories"]:
                        print(f"  {cat} <name> - Find entry in {cat}")
                        print(f"  add {cat} - Add new {cat}")

            elif command == "games":
                print("\nAvailable Games:")
                for g in manager.list_games():
                    print(f"  - {g}")

            elif command == "create" and len(args) > 1 and args[0] == "game":
                game_name = " ".join(args[1:])
                manager.create_game(game_name)

            elif command == "use":
                if not args:
                    print("Usage: use <game_name>")
                else:
                    game_name = " ".join(args)
                    manager.load_game(game_name)

            elif command == "export":
                if not args:
                    # Check for Android environment
                    is_android = "ANDROID_ROOT" in os.environ or \
                                 "ANDROID_DATA" in os.environ
                    if is_android:
                        # Common Termux path
                        default_path = "/sdcard/PalmonAssistantData"
                        print(f"Android detected. Defaulting export to: "
                              f"{default_path}")

                        game_mode = False
                        if len(args) > 1 and args[0] == "game":
                            game_mode = True

                        if game_mode and manager.current_game:
                            manager.export_data(default_path,
                                                manager.current_game.name)
                        elif game_mode:
                            print("No game selected to export.")
                        else:
                            manager.export_data(default_path)
                    else:
                        print("Usage: export <path> OR export game <path>")
                else:
                    if args[0] == "game":
                        if not manager.current_game:
                            print("No game selected to export.")
                        elif len(args) < 2:
                            print("Usage: export game <path>")
                        else:
                            manager.export_data(args[1],
                                                manager.current_game.name)
                    else:
                        manager.export_data(args[0])

            elif manager.current_game:
                # Dynamic commands for the current game
                game = manager.current_game
                if command == "add":
                    if not args:
                        print("Usage: add <category>")
                        continue
                    if args[0] == "category":
                        game.create_category()
                    else:
                        category = args[0]
                        game.add_entry(category)
                elif command in game.structure["categories"]:
                    if not args:
                        print(f"Usage: {command} <search_term>")
                    else:
                        search_term = " ".join(args)
                        game.find_entry(command, search_term)
                else:
                    print(f"Unknown command: '{command}'")
            else:
                print("No game selected. Use 'create game' or 'use'.")

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
