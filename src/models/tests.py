from re import M
import unittest
from unittest.mock import patch
from src.models.move import Move
from src.models.pokemon import Pokemon
from src.models.battle import Battle
import uuid


class Test(unittest.TestCase):
    def setUp(self):
        # Create two Pokemon instances for testing
        self.pokemon1 = Pokemon(id=1, name="Pikachu", level=20, hp=100, max_hp=100, attack=30, defense=50, speed=20, types=["electric"],
                                moves=[
                                    Move(name="Thunderbolt", type="electric", power=30, accuracy=100, pp=10, max_pp=10),
                                    Move(name="Quick Attack", type="normal", power=10, accuracy=100, pp=10, max_pp=10),
                                    Move(name="Thunder", type="electric", power=50, accuracy=100, pp=10, max_pp=10),
                                    Move(name="Agility", type="psychic", power=30, accuracy=100, pp=10, max_pp=10)
        ])
        self.pokemon2 = Pokemon(id=2, name="Charizard", level=20, hp=100, max_hp=100, attack=30, defense=50, speed=20, types=["fire"],
                                moves=[
                                    Move(name="Flamethrower", type="fire", power=30, accuracy=100, pp=10, max_pp=10),
                                    Move(name="Scratch", type="normal", power=10, accuracy=100, pp=10, max_pp=10),
                                    Move(name="Fire Blast", type="fire", power=50, accuracy=100, pp=10, max_pp=10),
                                    Move(name="Agility", type="psychic", power=30, accuracy=100, pp=10, max_pp=10)
        ])
        self.battle = Battle(_id=uuid.uuid4(), pokemon1=self.pokemon1, pokemon2=self.pokemon2, winner="", loser="", moves=[])

    def test_attack_rival(self):
        # Mock the randint function to return a specific value
        with patch("random.randint") as mock_randint:
            mock_randint.return_value = 1
            move, battle_moves = self.pokemon1.attack_rival(self.pokemon2, self.pokemon1.moves[0])

        # Assert that the move is updated correctly
        self.assertEqual(move.pp, 9)

        # Assert that the battle_moves list is updated correctly
        expected_battle_moves = ["Pikachu used Thunderbolt! PP 9/10", 'Charizard received 12 damage. HP 88/100\n']
        self.assertEqual(battle_moves, expected_battle_moves)

    def test_attack_rival_no_pp(self):
        # Mock the randint function to return a specific value
        with patch("random.randint") as mock_randint:
            mock_randint.return_value = 1
            # Set the PP of the move to 0
            self.pokemon1.moves[0].pp = 0
            move, battle_moves = self.pokemon1.attack_rival(self.pokemon2, self.pokemon1.moves[0])

        # Assert that the move is updated correctly
        self.assertEqual(move.pp, 0)

        # Assert that the battle_moves list is updated correctly
        expected_battle_moves = ['Pikachu want to use Thunderbolt but has no more PP!']
        self.assertEqual(battle_moves, expected_battle_moves)

    def test_receive_attack(self):

        self.pokemon1.receive_attack(10)
        # Assert that the pokemon's hp is updated correctly
        self.assertEqual(self.pokemon1.hp, 90)


if __name__ == "__main__":
    unittest.main()
