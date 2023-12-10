# Pokemon Battle field

Program that receives the names of 2 pokemons and simulates a battle between the two.
All pokemons data are fetched from the [PokeAPI](https://pokeapi.co/).

## Description

A Pokemon battle is a turn-based combat between two Pokémon. In these battles, trainers will command their Pokémon to use various moves to reduce the opponent's HP. When a Pokémon's HP is reduced to 0, it faints and can no longer battle. The trainer whose Pokémon all faints first loses.

A Pokemon has the following attributes:

- HP: Hit Points, defines how much damage a Pokémon can receive before fainting.
- Attack: Defines how much damage a Pokémon can inflict on another Pokémon.
- Defense: Defines how much damage a Pokémon can resist from another Pokémon's attack.
- Speed: Defines which Pokémon will attack first in a battle.
- Type: Defines the Pokémon's type, which determines the Pokémon's weaknesses and strengths.
- Moves: Defines the moves that a Pokémon can use in a battle.

To determine the winner of a battle between two Pokémon, we will consider various attributes and fields from the PokeAPI.
To calculate the damage inflicted by a Pokémon's attack, we will use the following formula (similar to the one used in the Pokémon games from Bulbapedia (https://bulbapedia.bulbagarden.net/wiki/Damage)):

```
Damage = ((((((2 * self.level * critical_hit)/5) + 2) * (self.attack / rival.defense) * move.power) / 50) + 2) * stab !
```

![damage formula](/docs/damage_formula.png)

Where:

- self.level: The level of the attacking Pokémon.
- critical_hit: A random number between 1 and 2. If the number is 1, then the attack is a critical hit, otherwise it is not.
- self.attack: The attack of the attacking Pokémon.
- rival.defense: The defense of the defending Pokémon.
- move.power: The power of the move used by the attacking Pokémon.
- stab: A random number between 1 and 1.5. If the attacking Pokémon's type is the same as the move's type, then the attack is a STAB (Same Type Attack Bonus), otherwise it is not.

The Pokémon with the highest damage inflicted wins the battle.
At the end of the battle, the program will print the winner and the loser, and the battle log will be saved in a MongoDB database.

## Battle

The battle will begin asking the user for the names of the two Pokemons.
The program will then fetch the data of the two Pokemons from the PokeAPI, and create two Pokemon objects.
The program will print the details of the two Pokemons.
The program will then create a Battle object, which will simulate the battle between the two Pokemons.
The Battle object will then print the winner and the loser, and save the battle log in a MongoDB database.
The rogramm will ask the user if they want to battle again, and if they do, the program will repeat the process.

## Implementation

The program is implemented in Python 3.8.5 and uses the libraries present in the requirements.txt file.
The database used is MongoDB, and the connection is made using the pymongo library.

The program is divided into 3 main modules:

- pokemon.py: Contains the Pokemon class, which represents a Pokemon and its attributes.
- move.py: Contains the Move class, which represents a move and its attributes.
- battle.py: Contains the Battle class, which represents a battle between two Pokemons.

The program also has 1 auxiliary module:

- src/app.py: Contains helper functions to fetch data from the PokeAPI and generate models from the data.

And 1 module to run the program:

- main.py: Contains the main function, which is responsible for receiving the names of the two Pokemons, fetching their data from the PokeAPI, and creating a Battle object to simulate the battle between the two Pokemons.

## Getting Started

### Dependencies

- Docker
- Docker-compose

### Installing and running

- git clone the project
- cd into the project folder
- run `make` to build the docker image and run the project
- run `make test` to run the tests (already runs when running `make`)
- run `make stop` to clean up the docker containers

## Author

Contributors names and contact info

[Alfonso Di Pace](https://www.linkedin.com/in/alfonsodipace/)

## License

This project is licensed under the [MIT] License - see the LICENSE.md file for details
