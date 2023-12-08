import logging
import random
import math
from pydantic import BaseModel


class Pokemon(BaseModel):
    """
    Pokemon model class that represents a pokemon
    """
    # pokemon id
    id: int
    # pokemon name
    name: str
    # pokemon level, higher level means higher stats
    level: int
    # hit points in a specific moment of the battle
    hp: int
    # total hit points
    max_hp: int
    # attack points used to calculate the damage
    attack: int
    # defense points used to calculate the damage
    defense: int
    # speed points used to determine the order of the pokemon in the battle
    speed: int
    # types is a list of the pokemon's types (e.g. fire, water, etc.)
    # used to calculate the STAB (same-type attack bonus)
    types: list
    # moves is a list of the pokemon's moves
    moves: list

    def attack_rival(self, rival, move):
        """
        Attack a rival pokemon with a move
        :param rival: the rival pokemon
        :param move: the move used to attack the rival pokemon
        :return: the move used to attack the rival pokemon and a list of strings that will be saved in the database to describe the battle
        """
        # battle_data is a list of strings that will be saved in the database to describe the battle
        battle_data = []

        # if the move has no more PP, the pokemon cannot use it
        # A move can only be used if the PP for that move is greater than 0.
        if move.pp == 0:
            logging.info("{0} want to use {1} but has no more PP!".format(self.name, move.name))
            battle_data.append("{0} want to use {1} but has no more PP!".format(self.name, move.name))
            return move, battle_data

        # PP is the power points. This is the number of times a move can be used.
        move.pp -= 1

        # Critical is 2 for a critical hit, and 1 otherwise.
        critical_hit = 1
        # critical_hit (10% chance)
        random_num = random.randint(1, 100)
        if random_num <= 10:
            critical_hit = 2

        # STAB is the same-type attack bonus. This is equal to 1.5 if the move's type matches any of the user's types, and 1 if otherwise.
        stab = 1
        if move.type in self.types:
            stab = 1.5

        # using a little simplified version of generation 1 from https://bulbapedia.bulbagarden.net/wiki/Damage
        # Damage is calculated using the following formula:
        damage = ((((((2 * self.level * critical_hit)/5) + 2) * (self.attack / rival.defense) * move.power) / 50) + 2) * stab

        # round down the damage
        damage = math.floor(damage)

        # the damage is subtracted from the rival's HP, which cannot go below zero.
        rival.receive_attack(damage)

        logging.info("{0} used {1}! PP {2}/{3}".format(self.name, move.name, move.pp, move.max_pp))
        logging.info("{0} received {1} damage. HP {2}/{3}\n".format(rival.name, damage, rival.hp, rival.max_hp))
        battle_data.append("{0} used {1}! PP {2}/{3}".format(self.name, move.name, move.pp, move.max_pp))
        battle_data.append("{0} received {1} damage. HP {2}/{3}\n".format(rival.name, damage, rival.hp, rival.max_hp))

        return move, battle_data

    def receive_attack(self, damage):
        """
        Receive an attack from a rival pokemon.
        The damage is subtracted from the pokemon's HP, which cannot go below zero.
        :param damage: the damage received from the rival pokemon
        """
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def __str__(self):
        return "Pokemon: {0}\nLevel: {1}\nHP: {2}/{3}\nAttack: {4}\nDefense: {5}\nSpeed: {6}\nTypes: {7}\nMoves: {8}".format(
            self.name, self.level, self.hp, self.max_hp, self.attack, self.defense, self.speed, self.types, self.moves)
