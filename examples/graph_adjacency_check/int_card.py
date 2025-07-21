# Import the abstact card class
from pygame_cards.abstract import AbstractCard
# from int_card_graphics import IntCardGraphics
# from pathlib import Path

from dataclasses import dataclass


@dataclass
class IntCard(AbstractCard):
    face_up: bool
    
    # def flip_card(self):
    #     """Toggle the face_up state of the card."""
    #     if self.face_up:
    #         self.face_up = False
    #         self.graphics = IntCardGraphics(
    #                 self,
    #                 filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
    #         )
    #     else:
    #         self.face_up = True
    #         self.graphics = IntCardGraphics(
    #                 self,
    #                 filepath=Path("examples/pushmerge_zkp/images", f"{self.number}.png"),
    #         )

if __name__ == "__main__":
    card = IntCard(
        number=1,
        face_up=False,
    )
    print(card)
