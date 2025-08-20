from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
import sys
from time import sleep
import pygame
from suit_card import SuitCard

from pygame_emojis import load_emoji

# Again, we start from the abstract graphics
from pygame_cards.abstract import AbstractCardGraphics

# Import the cards we just created
from letter_set import ADJACENCY_COL_1, ADJACENCY_COL_2, ADJACENCY_COL_3, ADJACENCY_COL_4, ADJACENCY_COL_5, ADJACENCY_COL_6, ADJACENCY_COL_1_COPY, ADJACENCY_COL_2_COPY, ADJACENCY_COL_3_COPY, ADJACENCY_COL_4_COPY, ADJACENCY_COL_5_COPY, ADJACENCY_COL_6_COPY
from pygame_cards.utils import position_for_centering


@dataclass
class LetterCardGraphics(AbstractCardGraphics):

    # Specify the type of card that this graphics accept
    card: SuitCard

    # This will be the file where the character is
    filepath: Path = None

    @cached_property
    def surface(self) -> pygame.Surface:
        # Size is a property from AbstractCardGraphics
        x, y = self.size

        # Create the surface on which we will plot the card
        surf = pygame.Surface(self.size)

        if self.filepath is not None:
            # Load the image of our character
            picture = pygame.image.load(self.filepath)
            # Rescale it to fit the surface
            surf.blit(pygame.transform.scale(picture, self.size), (0, 0))

        return surf


for card in ADJACENCY_COL_1 + ADJACENCY_COL_2 + ADJACENCY_COL_3 + ADJACENCY_COL_4 + ADJACENCY_COL_5 + ADJACENCY_COL_6 + ADJACENCY_COL_1_COPY + ADJACENCY_COL_2_COPY + ADJACENCY_COL_3_COPY + ADJACENCY_COL_4_COPY + ADJACENCY_COL_5_COPY + ADJACENCY_COL_6_COPY:
    match card.name:
        case "N":
            if card.face_up:
                file = (
                    "N.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "S":
            if card.face_up:
                file = (
                    "S.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "E":
            if card.face_up:
                file = (
                    "E.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "W":
            if card.face_up:
                file = (
                    "W.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "X":
            if card.face_up:
                file = (
                    "X.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "O":
            if card.face_up:
                file = (
                    "O.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "blank":
            file = (
                "blank.png"
            )
        case _:
            raise ValueError(f"Unknown character {card.name}")

    card.graphics = LetterCardGraphics(
        card,
        filepath=Path("examples/scrn/images", file),
    )

if __name__ == "__main__":
    # A very simple game loop to show the cards
    pygame.init()

    size = width, height = 1000, 500

    screen = pygame.display.set_mode(size)
    screen.fill("black")

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()

        # Make sure you don't burn your cpu
        sleep(1)