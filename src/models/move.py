from typing import Optional
from pydantic import BaseModel


class Move(BaseModel):
    """
    Move model class that represents a move
    """
    # move name
    name: str
    # move type (e.g. fire, water, etc.)
    # used to calculate the STAB (same-type attack bonus)
    type: str
    # move power
    # used to calculate the damage
    power: int
    # move accuracy
    # can be used to calculate if the move hits the rival pokemon
    accuracy: Optional[int] = 100
    # move power points
    # A move can only be used if the PP for that move is greater than 0.
    pp: int
    # move max power points
    # PP is the power points. This is the number of times a move can be used.
    max_pp: int

    def __str__(self):
        return "\nMove: {0}, Type: {1}, Power: {2}, Accuracy: {3}, PP: {4}".format(self.name, self.type, self.power,
                                                                                   self.accuracy, self.pp)

    def __repr__(self):
        return "\nMove: {0}, Type: {1}, Power: {2}, Accuracy: {3}, PP: {4}".format(self.name, self.type, self.power,
                                                                                   self.accuracy, self.pp)
