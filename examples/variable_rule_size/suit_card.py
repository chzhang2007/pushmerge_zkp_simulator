# Import the abstact card class
from pygame_cards.abstract import AbstractCard

from dataclasses import dataclass


@dataclass
class SuitCard(AbstractCard):
    face_up: bool # False = face down, True = face up

if __name__ == "__main__":
    card = SuitCard(
        face_up=False,
    )
    print(card)
