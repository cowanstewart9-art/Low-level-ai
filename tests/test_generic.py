import unittest
import os
import json
import shutil
from palmon_assistant.assistant import GameManager, Game

class TestGenericAssistant(unittest.TestCase):
    def setUp(self):
        # Setup a temporary test environment
        self.test_games_dir = "data/games_test"
        # Patch the GAMES_DIR in the module (dirty but effective for simple script)
        import palmon_assistant.assistant
        palmon_assistant.assistant.GAMES_DIR = self.test_games_dir

        if os.path.exists(self.test_games_dir):
            shutil.rmtree(self.test_games_dir)
        os.makedirs(self.test_games_dir)

    def tearDown(self):
        if os.path.exists(self.test_games_dir):
            shutil.rmtree(self.test_games_dir)

    def test_create_game(self):
        manager = GameManager()
        manager.create_game("Test Game")
        self.assertTrue(os.path.exists(os.path.join(self.test_games_dir, "Test Game")))
        self.assertTrue(os.path.exists(os.path.join(self.test_games_dir, "Test Game", "structure.json")))

    def test_create_category_single_file(self):
        manager = GameManager()
        manager.create_game("Test Game")
        game = manager.current_game

        # New default behavior creates single-file structure
        self.assertEqual(game.structure.get("storage_mode"), "single_file")

        # Add category manually to structure
        game.structure["categories"]["unit"] = {
            "key_field": "name",
            "fields": ["hp", "attack"]
        }
        game._save_structure()

        if "unit" not in game.data:
            game.data["unit"] = []

        game.save_data("unit") # Should save to Test Game.json

        # Check that individual file does NOT exist
        self.assertFalse(os.path.exists(os.path.join(self.test_games_dir, "Test Game", "units.json")))

        # Check that single data file DOES exist
        self.assertTrue(os.path.exists(os.path.join(self.test_games_dir, "Test Game", "Test Game.json")))

        # Test adding entry
        game.data["unit"].append({"name": "Warrior", "hp": 100, "attack": 10})
        game.save_data("unit")

        # Reload to verify
        game2 = Game("Test Game")
        self.assertEqual(len(game2.data["unit"]), 1)
        self.assertEqual(game2.data["unit"][0]["name"], "Warrior")

    def test_export_data(self):
        manager = GameManager()
        manager.create_game("ExportGame")

        # Create dummy data
        game = manager.current_game
        game.structure["categories"]["test"] = {"key_field": "id", "fields": ["val"]}
        game.data["test"] = [{"id": "1", "val": "A"}]
        game.save_data()

        export_path = os.path.join(self.test_games_dir, "export_out")
        manager.export_data(export_path)

        self.assertTrue(os.path.exists(os.path.join(export_path, "ExportGame", "ExportGame.json")))
        self.assertTrue(os.path.exists(os.path.join(export_path, "ExportGame", "structure.json")))


if __name__ == '__main__':
    unittest.main()
