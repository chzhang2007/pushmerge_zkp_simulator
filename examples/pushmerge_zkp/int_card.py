# Import the abstact card class
from pygame_cards.abstract import AbstractCard

from dataclasses import dataclass


@dataclass
class IntCard(AbstractCard):
    face_up: bool

if __name__ == "__main__":
    card = IntCard(
        face_up=False,
    )
    print(card)
