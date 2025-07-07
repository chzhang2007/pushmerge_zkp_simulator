# Import the abstact card class
from pygame_cards.abstract import AbstractCard

from dataclasses import dataclass


@dataclass
class SuitCard(AbstractCard):
    x: int
    y: int
    suit: int # 0 = hearts, 1 = spades, 2 = clubs, 3 = diamonds

    description: str = ""


if __name__ == "__main__":
    card = SuitCard(
        name="heart",
        x=100,
        y=200,
        suit=0,
    )

    print(card)
