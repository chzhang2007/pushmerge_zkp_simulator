# Import the abstact card class
from pygame_cards.abstract import AbstractCard
# from int_card_graphics import IntCardGraphics
# from pathlib import Path

from dataclasses import dataclass


@dataclass
class IntCard(AbstractCard):
    number: int
    face_up: bool

if __name__ == "__main__":
    card = IntCard(
        number=1,
        face_up=False,
    )
    print(card)
