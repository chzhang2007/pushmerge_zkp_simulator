import random
import sys
import pygame
from pathlib import Path
from suit_card_graphics import SuitCardGraphics
from int_card_graphics import IntCardGraphics
from pygame_cards.abstract import AbstractCard
from pygame_cards.back import CardBackGraphics
from pygame_cards.hands import AlignedHand, AlignedHandVertical
from pygame_cards.manager import CardSetRights, CardsManager

from suit_set import GRID_STATE
from int_set import ID20
from pygame_cards.set import CardsSet

pygame.init()


screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
# screen = pygame.display.set_mode((400, 300))
size = width, height = screen.get_size()


manager = CardsManager()


# Creates your card set
id_cards = ID20.copy()
grid_state = GRID_STATE.copy()

card_size = (width / 21, height / 9 - 10)
card_set_size_wide = (width - 10, height / 9)

id_cards_graphics = AlignedHand(
    id_cards,
    card_set_size_wide,
    card_size=card_size,
    graphics_type=IntCardGraphics,
)
# Finally add the set to the manager
manager.add_set(
    id_cards_graphics,
    # Position on the screen of the entire set
    (0, 0),
)
grid_state_graphics = AlignedHand(
        grid_state,
        card_set_size_wide,
        card_size=card_size,
        graphics_type=SuitCardGraphics,
    )

manager.add_set(
    grid_state_graphics,
    # Position on the screen of the entire set
    (0, id_cards_graphics.size[1] + 10),
)

card_back = AbstractCard("")
card_back.graphics_type = CardBackGraphics

pygame.display.flip()

clock = pygame.time.Clock()

stage = 0 # 0 = everything face-up, 1 = everything face-down

while 1: # game loop
    screen.fill("black")
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 0:
            for card in id_cards_graphics.cardset:
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
            for card in grid_state_graphics.cardset:
                card.face_up = False
                card.graphics = SuitCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
            stage = 1
            id_cards_graphics.clear_cache()
            grid_state_graphics.clear_cache()
    
        manager.process_events(event)

    manager.update(time_delta)
    manager.draw(screen)
    pygame.display.flip()