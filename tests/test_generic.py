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

    def test_create_category(self):
        manager = GameManager()
        manager.create_game("Test Game")
        game = manager.current_game

        # Simulate input for create_category
        # Input: name, key_field, fields
        # Using a mock or just modifying structure directly for unit test logic
        game.structure["categories"]["unit"] = {
            "file": "units.json",
            "key_field": "name",
            "fields": ["hp", "attack"]
        }
        game._save_structure()
        game.data["unit"] = []
        game.save_data("unit")

        self.assertTrue(os.path.exists(os.path.join(self.test_games_dir, "Test Game", "units.json")))

        # Test adding entry
        game.data["unit"].append({"name": "Warrior", "hp": 100, "attack": 10})
        game.save_data("unit")

        # Reload to verify
        game2 = Game("Test Game")
        self.assertEqual(len(game2.data["unit"]), 1)
        self.assertEqual(game2.data["unit"][0]["name"], "Warrior")

if __name__ == '__main__':
    unittest.main()
