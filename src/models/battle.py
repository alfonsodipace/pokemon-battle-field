import logging
import random
from pydantic import UUID4, BaseModel
from pymongo import errors

from src.models.pokemon import Pokemon


class Battle(BaseModel):
    """
    Battle model class that represents a battle between two pokemon
    """
    # battle id
    _id: UUID4
    # pokemon1 and pokemon2 are the two pokemon that will battle
    pokemon1: Pokemon
    # pokemon1 and pokemon2 are the two pokemon that will battle
    pokemon2: Pokemon
    # winner and loser are the names of the pokemon that won and lost the battle
    winner: str
    # winner and loser are the names of the pokemon that won and lost the battle
    loser: str
    # moves is a list of the moves that were performed in the battle
    moves: list

    def perform_battle(self):
        """
        Perform the battle.
        In each turn, each pokemon attacks the other pokemon and vice versa
        """
        # the turn is exececuted only if both pokemon have at least one move with PP > 0
        # and if both pokemon have HP > 0
        while self.pokemon1.hp > 0 and self.pokemon2.hp > 0 and (sum([move.pp for move in self.pokemon1.moves]) > 0 and sum([move.pp for move in self.pokemon2.moves]) > 0):
            # pokemon1 attacks pokemon2
            rand1 = random.randint(0, len(self.pokemon1.moves) - 1)
            move1, battle_moves1 = self.pokemon1.attack_rival(self.pokemon2, self.pokemon1.moves[rand1])
            self.pokemon1.moves[rand1] = move1
            self.moves.append(battle_moves1)
            if self.pokemon2.hp == 0:
                break

            # pokemon2 attacks pokemon1
            rand2 = random.randint(0, len(self.pokemon2.moves) - 1)
            move2, battle_moves2 = self.pokemon2.attack_rival(self.pokemon1, self.pokemon2.moves[rand2])
            self.pokemon2.moves[rand2] = move2
            self.moves.append(battle_moves2)
            if self.pokemon1.hp == 0:
                break

        # if one Pokémon's HP drops to zero or below, that Pokémon loses the battle.
        # the Pokémon with higher remaining HP at the end of the simulation is the winner.
        if self.pokemon1.hp > 0:
            self.winner = self.pokemon1.name
            self.loser = self.pokemon2.name
            logging.info("{0} won!".format(self.pokemon1.name))
            self.moves.append(["{0} won!".format(self.pokemon1.name)])
        else:
            self.winner = self.pokemon2.name
            self.loser = self.pokemon1.name
            logging.info("{0} won!".format(self.pokemon2.name))
            self.moves.append(["{0} won!".format(self.pokemon2.name)])

    def save_to_db(self, collection):
        """
        Save the battle to the database
        :param collection: the collection where the battle will be saved
        """
        battle_json = self.model_dump()
        try:
            collection.insert_one(document=battle_json)
        except errors.PyMongoError as e:
            logging.error('Unable to insert battle to DB!\n{0}'.format(e))
            raise e
        else:
            logging.info("Battle saved to the database.")
            logging.info("Battle id: {0}".format(battle_json["_id"]))

    def __str__(self):
        return "\nBattle id: {0}, Pokemon1: {1}, Pokemon2: {2}, Winner: {3}, Loser: {4}".format(self._id, self.pokemon1,
                                                                                                self.pokemon2,
                                                                                                self.winner,
                                                                                                self.loser)

    def __repr__(self):
        return "\nBattle id: {0}, Pokemon1: {1}, Pokemon2: {2}, Winner: {3}, Loser: {4}".format(self._id, self.pokemon1,
                                                                                                self.pokemon2,
                                                                                                self.winner,
                                                                                                self.loser)
