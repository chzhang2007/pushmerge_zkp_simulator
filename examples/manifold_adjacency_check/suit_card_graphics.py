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
from suit_set import MANIFOLD_STATE, AE, AE_2, AG, AG_2
from pygame_cards.utils import position_for_centering


@dataclass
class SuitCardGraphics(AbstractCardGraphics):

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


for card in MANIFOLD_STATE + AE + AE_2 + AG + AG_2:
    match card.name:
        case "heart":
            if card.face_up:
                file = (
                    "heart.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "spade":
            if card.face_up:
                file = (
                    "spade.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "club":
            if card.face_up:
                file = (
                    "club.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "diamond":
            if card.face_up:
                file = (
                    "diamond.png"
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
            raise ValueError(f"Unkonwn character {card.name}")

    card.graphics = SuitCardGraphics(
        card,
        filepath=Path("examples/manifold_adjacency_check/images", file),
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
