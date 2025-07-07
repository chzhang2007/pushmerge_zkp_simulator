# Import the abstact card class
from pygame_cards.abstract import AbstractCard

from dataclasses import dataclass


@dataclass
class SuitCard(AbstractCard):
    suit: int # 0 = hearts, 1 = spades, 2 = clubs, 3 = diamonds

if __name__ == "__main__":
    card = SuitCard(
        suit=0,
    )
    print(card)
