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
from suit_set import ABB_CARDS, AEB_CARDS, AEE_CARDS, AED_CARDS, DUMMY_LENGTH_2, GRID_STATE, BB_CARDS, BB_CARDS2, BB_CARDS3, BB_CARDS4, BD_CARDS, BD_CARDS2, BD_CARDS3, BD_CARDS4, BE_CARDS, BE_CARDS2, BE_CARDS3, BE_CARDS4, DB_CARDS, DB_CARDS2, DB_CARDS3, DB_CARDS4, DD_CARDS, DD_CARDS2, DD_CARDS3, DD_CARDS4, DE_CARDS, DE_CARDS2, DE_CARDS3, DE_CARDS4, EB_CARDS, EB_CARDS2, EB_CARDS3, EB_CARDS4, ED_CARDS, ED_CARDS2, ED_CARDS3, ED_CARDS4, EE_CARDS, EE_CARDS2, EE_CARDS3, EE_CARDS4, ABB_CARDSQ, AEB_CARDSQ, AED_CARDSQ, AEE_CARDSQ, B, D, E, DUMMY
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


for card in ABB_CARDS + AEB_CARDS + AEE_CARDS + AED_CARDS + DUMMY_LENGTH_2 + GRID_STATE + BB_CARDS + BB_CARDS2 + BB_CARDS3 + BB_CARDS4 + BD_CARDS + BD_CARDS2 + BD_CARDS3 + BD_CARDS4 + BE_CARDS + BE_CARDS2 + BE_CARDS3 + BE_CARDS4 + DB_CARDS + DB_CARDS2 + DB_CARDS3 + DB_CARDS4 + DD_CARDS + DD_CARDS2 + DD_CARDS3 + DD_CARDS4 + DE_CARDS + DE_CARDS2 + DE_CARDS3 + DE_CARDS4 + EB_CARDS + EB_CARDS2 + EB_CARDS3 + EB_CARDS4 + ED_CARDS + ED_CARDS2 + ED_CARDS3 + ED_CARDS4 + EE_CARDS + EE_CARDS2 + EE_CARDS3 + EE_CARDS4 + ABB_CARDSQ + AEB_CARDSQ + AED_CARDSQ + AEE_CARDSQ + B + D + E + DUMMY:
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
        filepath=Path("examples/variable_rule_size/images", file),
    )

if __name__ == "__main__":
    # A very simple game loop to show the cards
    pygame.init()

    size = width, height = 1000, 500

    screen = pygame.display.set_mode(size)
    screen.fill("black")

    for i, card in enumerate(ABB_CARDS):
        position = (0, i * card.graphics.size[1]) # edit this to change card positions within a block

        # Simply blit the card on the main surface
        screen.blit(card.graphics.surface, position)
        
    for i, card in enumerate(AEB_CARDS):
        position = (card.graphics.size[0] + 10, i * card.graphics.size[1]) # edit this to change card positions within a block

        # Simply blit the card on the main surface
        screen.blit(card.graphics.surface, position)
        
    for i, card in enumerate(AEE_CARDS):
        position = (2 * card.graphics.size[0] + 20, i * card.graphics.size[1]) # edit this to change card positions

        # Simply blit the card on the main surface
        screen.blit(card.graphics.surface, position)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pygame.display.flip()

        # Make sure you don't burn your cpu
        sleep(1)
