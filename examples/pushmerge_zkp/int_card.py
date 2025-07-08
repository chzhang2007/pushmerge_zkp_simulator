# Import the abstact card class
from pygame_cards.abstract import AbstractCard

from dataclasses import dataclass


@dataclass
class IntCard(AbstractCard):
    number: int

if __name__ == "__main__":
    card = IntCard(
        number=1,
    )
    print(card)
