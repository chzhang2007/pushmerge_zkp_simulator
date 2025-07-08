from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
import sys
from time import sleep
import pygame
from int_card import IntCard

from pygame_emojis import load_emoji

# Again, we start from the abstract graphics
from pygame_cards.abstract import AbstractCardGraphics

# Import the cards we just created
from int_set import ID3
from pygame_cards.utils import position_for_centering


@dataclass
class IntCardGraphics(AbstractCardGraphics):

    # Specify the type of card that this graphics accept
    card: IntCard

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

for card in ID3:
    match card.name:
        case "0":
            if card.face_up:
                file = (
                    "0.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "1":
            if card.face_up:
                file = (
                    "1.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "2":
            if card.face_up:
                file = (
                    "2.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "3":
            if card.face_up:
                file = (
                    "3.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "4":
            if card.face_up:
                file = (
                    "4.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case "5":
            if card.face_up:
                file = (
                    "5.png"
                )
            else:
                # If the card is face down, we use the back of the card
                file = (
                    "card_back.png"
                )
        case _:
            raise ValueError(f"Unkonwn character {card.name}")

    card.graphics = IntCardGraphics(
        card,
        filepath=Path("examples/pushmerge_zkp/images", file),
    )

if __name__ == "__main__":
    # A very simple game loop to show the cards
    pygame.init()

    size = width, height = 1000, 500

    screen = pygame.display.set_mode(size)
    screen.fill("black")

    for i, card in enumerate(ID3):
        position = (50 + i * (100 + card.graphics.size[0]), 20) # edit this to change card positions

        # Simply blit the card on the main surface
        screen.blit(card.graphics.surface, position)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()

        # Make sure you don't burn your cpu
        sleep(1)
