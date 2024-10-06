import unittest
from unittest.mock import patch
import string

class TestTreasureMap(unittest.TestCase):
    def setUp(self):
        self.map = TreasureMap(size=10)

    @patch('random.randint', return_value=5)
    @patch('random.choice', return_value='e')
    def test_generate_treasure_position(self, mock_randint, mock_choice):
        self.map.treasure_position = self.map.generate_treasure_position()
        self.assertEqual(self.map.treasure_position, (5, 'e'))

    def test_is_treasure(self):
        self.map.treasure_position = (5, 'e')
        self.assertTrue(self.map.is_treasure(5, 'e'))
        self.assertFalse(self.map.is_treasure(0, 'a'))

    def test_give_hint(self):
        self.map.treasure_position = (5, 'e')
        self.assertEqual(self.map.give_hint(5, 'e'), "Поздравляем! Вы нашли сокровище.")
        self.assertEqual(self.map.give_hint(4, 'e'), "Вы очень близко к сокровищу!")
        self.assertEqual(self.map.give_hint(0, 'a'), "Вы далеко от сокровища.")


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(attempts=10)

    def test_make_guess_valid(self):
        self.assertEqual(self.player.make_guess('5, e'), (5, 'e'))
        self.assertEqual(self.player.make_guess('0, a'), (0, 'a'))

    def test_make_guess_invalid(self):
        self.assertIsNone(self.player.make_guess('invalid input'))
        self.assertIsNone(self.player.make_guess('5, z'))  # out of bounds letter
        self.assertIsNone(self.player.make_guess('-1, a'))  # out of bounds number


class TestGame(unittest.TestCase):
    @patch('builtins.input', side_effect=['5, e', '7, b', '5, e'])
    def test_game_flow(self, mock_input):
        game = Game()
        game.map.treasure_position = (5, 'e')  # Mock treasure position
        with patch('builtins.print') as mock_print:  # Mock print for game output
            game.start()
        self.assertTrue(game.is_game_over)


if __name__ == '__main__':
    unittest.main()
