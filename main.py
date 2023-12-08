import logging
import random
from src.app import get_input_pokemon
from database.db_config import get_db_info
import sys
from src.models.battle import Battle
import uuid
from pymongo import MongoClient, errors

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# get the database information from the db_info.ini file
filename = 'db_info.ini'
section = 'mongo-db'
db_info = get_db_info(filename, section)

# connect to the database
try:
    client = MongoClient('mongodb://mongo:27017', username="username", password="secret", authSource="pokemon", authMechanism="SCRAM-SHA-256", uuidRepresentation='standard')
    db = client['pokemon']
    collection = db['battle']
except errors.ConnectionFailure as e:
    logging.error('Unable to connect to DB!\n{0}'.format(e))
    sys.exit(1)
else:
    logging.info("Successfully connected to the database.")

if __name__ == '__main__':
    logging.info("Starting the pokemon battle...")

    battle_again = True
    while battle_again:
        # set the level of the pokemon
        level = random.randint(10, 30)
        # get the pokemon names from the user input and generate the pokemons
        pokemon1 = get_input_pokemon(level, 1)
        pokemon2 = get_input_pokemon(level, 2)

        # set the order of the pokemon in the battle
        if pokemon2.speed > pokemon1.speed:
            pokemon1, pokemon2 = pokemon2, pokemon1

        logging.info("The battle begins!\n")

        # battle
        battle = {
            '_id': str(uuid.uuid4()),
            'pokemon1': pokemon1,
            'pokemon2': pokemon2,
            'winner': "",
            'loser': "",
            'moves': [],
        }
        battle = Battle(**battle)
        battle.perform_battle()

        # save the battle to the database
        battle.save_to_db(collection)

        # ask the user if they want to battle again
        while True:
            inp = input('Do you want to battle again? (y/n): ')
            if inp == 'y' or inp == 'n':
                if inp == 'y':
                    logging.info("Starting a new battle...")
                    battle_again = True
                else:
                    logging.info("Exiting the pokemon battle...")
                    battle_again = False
                break
            else:
                continue
