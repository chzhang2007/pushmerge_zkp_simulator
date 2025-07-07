import sys
import pygame
from suit_card_graphics import SuitCardGraphics
from pygame_cards.abstract import AbstractCard
from pygame_cards.back import CardBackGraphics
from pygame_cards.hands import AlignedHand
from pygame_cards.manager import CardSetRights, CardsManager

from suit_set import SUIT_CARDS
from pygame_cards.set import CardsSet

pygame.init()


screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
# screen = pygame.display.set_mode((400, 300))
size = width, height = screen.get_size()
print(size)


manager = CardsManager()


# Creates your card set
my_cards = SUIT_CARDS.copy()


card_size = (width / 7, height / 3 - 20)
card_set_size = (width / 2, height / 3)
my_cards_graphics = AlignedHand(
    my_cards,
    card_set_size,
    card_size=card_size,
    graphics_type=SuitCardGraphics,
)
# Finally add the set to the manager
manager.add_set(
    my_cards_graphics,
    # Position on the screen
    (width / 4, height - my_cards_graphics.size[1]),
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
