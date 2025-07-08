import random
import sys
import pygame
from suit_card_graphics import SuitCardGraphics
from int_card_graphics import IntCardGraphics
from pygame_cards.abstract import AbstractCard
from pygame_cards.back import CardBackGraphics
from pygame_cards.hands import AlignedHand
from pygame_cards.manager import CardSetRights, CardsManager

from suit_set import ABB_CARDS, AEB_CARDS, AEE_CARDS
from int_set import INT_CARDS
from pygame_cards.set import CardsSet

pygame.init()


screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
# screen = pygame.display.set_mode((400, 300))
size = width, height = screen.get_size()
print(size)


manager = CardsManager()


# Creates your card set
abb_cards = ABB_CARDS.copy()
aeb_cards = AEB_CARDS.copy()
aee_cards = AEE_CARDS.copy()
int_cards = INT_CARDS.copy()
random.shuffle(int_cards)


card_size = (width / 14, height / 6 - 10)
card_set_size_wide = (width / 4, height / 6)
card_set_size_long = (width / 10, height / 2)
abb_cards_graphics = AlignedHand(
    abb_cards,
    card_set_size_long,
    card_size=card_size,
    graphics_type=SuitCardGraphics,
)
# Finally add the set to the manager
manager.add_set(
    abb_cards_graphics,
    # Position on the screen of the entire set
    (width / 6, abb_cards_graphics.size[1] + 20),
)
int_cards_graphics = AlignedHand(
    int_cards,
    card_set_size_wide,
    card_size=card_size,
    graphics_type=IntCardGraphics,
)
# Finally add the set to the manager
manager.add_set(
    int_cards_graphics,
    # Position on the screen of the entire set
    (width / 6, 0),
)

card_back = AbstractCard("")
card_back.graphics_type = CardBackGraphics

pygame.display.flip()

clock = pygame.time.Clock()

annimation_tick_left = 0

while 1: # game loop
    screen.fill("black")
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        manager.process_events(event)

    manager.update(time_delta)
    manager.draw(screen)
    pygame.display.flip()
