import math
from sys import version
import requests
from functools import lru_cache
import logging

from src.models.move import Move
from src.models.pokemon import Pokemon


def get_input_pokemon(level, pokemon_number):
    """
    Ask the user to input the name of the pokemon
    :param level: the level of the pokemon
    :param pokemon_number: the number of the pokemon
    :return: the pokemon
    """
    while True:
        try:
            inp = input('Enter the name of pokemon {0}: '.format(pokemon_number))
            if inp == '' or inp.isspace():
                logging.error('Pokemon name cannot be empty')
                continue
            inp = inp.lower()
            pokemon = generate_pokemon(inp, level)
            logging.info("Pokemon{0}: {1}\n".format(pokemon_number, pokemon))
        # in case the pokemon is not found
        except requests.exceptions.HTTPError:
            continue
        else:
            break

    return pokemon


def generate_pokemon(name, level):
    """
    Generate a pokemon with the given name and level
    :param name: the name of the pokemon
    :param level: the level of the pokemon
    :return: the pokemon
    """

    logging.info("Fetching pokemon data for {0}".format(name))
    json_pokemon = get_pokemon_data(name)

    logging.info("FOUND! Generating pokemon {0} with level {1}".format(name, level))

    # initialize the pokemon
    pokemon = {
        'id': json_pokemon['id'],
        'name': name,
        'level': level,
    }

    # get the pokemon's stats from the API
    stats = json_pokemon['stats']
    for stat in stats:
        if stat['stat']['name'] == 'hp':
            pokemon["hp"] = stat['base_stat'] + level
            pokemon["max_hp"] = stat['base_stat'] + level
        elif stat['stat']['name'] == 'attack':
            pokemon["attack"] = stat['base_stat']
        elif stat['stat']['name'] == 'defense':
            pokemon["defense"] = stat['base_stat']
        elif stat['stat']['name'] == 'speed':
            pokemon["speed"] = stat['base_stat']

    # set the pokemon's types
    types = []
    for i in range(len(json_pokemon['types'])):
        type = json_pokemon['types'][i]
        types.append(type['type']['name'])

    pokemon["types"] = types

    #  get the pokemon's moves from the API
    logging.info("{0} has {1} moves".format(name, len(json_pokemon['moves'])))
    logging.info("Fetching moves for {0}".format(name))
    moves = []
    with requests.Session() as session:
        for i in range(len(json_pokemon['moves'])):
            # selecting only moves that can be learned by level up to avoid too many API calls
            version_group_details = json_pokemon['moves'][i]['version_group_details']
            for j in range(len(version_group_details)):
                if version_group_details[j]['move_learn_method']['name'] != 'level-up':
                    continue
                else:
                    move = generate_move(json_pokemon['moves'][i]['move']['url'], session)
                    # filter only attacking moves
                    if move["power"] is not None:
                        moves.append(Move(**move))
                    break

    logging.info("Selecting for you the best 4 moves...")
    # sort the moves by power
    moves.sort(key=lambda x: x.power, reverse=True)
    # get only the top 4 moves
    if len(moves) > 4:
        moves = moves[:4]

    pokemon["moves"] = moves

    return Pokemon(**pokemon)


def generate_move(url, session):
    """
    Generate a move with the given url
    :param url: the url of the move
    :return: the move
    """
    try:
        res = get_move_data(url, session)
        move = {
            'name': res['name'],
            'type': res['type']['name'],
            'accuracy': res['accuracy'],
            'pp': res['pp'],
            'max_pp': res['pp'],
        }
        if res['power'] is not None:
            move["power"] = math.floor(res['power']/10)
        else:
            move["power"] = None
    except requests.exceptions.RequestException as e:
        logging.error("An error occurred:", e)
        raise e

    return move


@lru_cache(maxsize=None)
def get_pokemon_data(name):
    """
    Get the pokemon data from the API.
    Use lru_cache to cache the results of the API calls
    :param name: the name of the pokemon
    :return: the pokemon data
    """
    try:
        res = requests.get('https://pokeapi.co/api/v2/pokemon/{0}'.format(name))
        res.raise_for_status()  # Raise an exception for unsuccessful HTTP status codes
        json_pokemon = res.json()
        return json_pokemon
    except requests.exceptions.HTTPError as errh:
        if errh.response.status_code == 404:
            logging.warning("Pokemon not found! Try again.")
            raise errh
        logging.error("Http Error:", errh)
        raise errh
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting:", errc)
        raise errc
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error:", errt)
        raise errt
    except requests.exceptions.JSONDecodeError as errj:
        logging.error("JSON Decode Error:", errj)
        raise errj
    except requests.exceptions.RequestException as err:
        logging.error("OOps: Something Else", err)
        raise err


@lru_cache(maxsize=None)
def get_move_data(url, session):
    """
    Get the move data from the API.
    Use lru_cache to cache the results of the API calls
    :param url: the url of the move
    :return: the move data
    """
    try:
        res = session.get(url)
        res.raise_for_status()  # Raise an exception for unsuccessful HTTP status codes
        return res.json()
    except requests.exceptions.HTTPError as errh:
        if errh.response.status_code == 404:
            logging.warning("Move not found! Try again.")
            raise errh
        logging.error("Http Error:", errh)
        raise errh
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting:", errc)
        raise errc
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error:", errt)
        raise errt
    except requests.exceptions.JSONDecodeError as errj:
        logging.error("JSON Decode Error:", errj)
        raise errj
    except requests.exceptions.RequestException as err:
        logging.error("OOps: Something Else", err)
        raise err
