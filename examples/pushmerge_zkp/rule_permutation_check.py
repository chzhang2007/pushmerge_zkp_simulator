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

from suit_set import ABB_CARDS, AEB_CARDS, AEE_CARDS, AED_CARDS
from int_set import ID4
from pygame_cards.set import CardsSet

pygame.init()


screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
# screen = pygame.display.set_mode((400, 300))
size = width, height = screen.get_size()


manager = CardsManager()


# Creates your card set
col_cards = [ABB_CARDS.copy(), AEB_CARDS.copy(), AEE_CARDS.copy(), AED_CARDS.copy()] # col_cards[i] is the (i + 1)th column of cards
int_cards = ID4.copy()

card_size = (width / 14, height / 6 - 10)
card_set_size_wide = (width / 3, height / 6)
card_set_size_long = (width / 12, height / 2)

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

col_cards_graphics = [(AlignedHandVertical(
                        col_cards[i],
                        card_set_size_long,
                        card_size=card_size,
                        graphics_type=SuitCardGraphics,
                    )) for i in range(len(col_cards))]
manager.add_set(
    col_cards_graphics[0],
    # Position on the screen of the entire set
    (width / 6 - 5, int_cards_graphics.size[1] + 20),
)
manager.add_set(
    col_cards_graphics[1],
    # Position on the screen of the entire set
    (width / 4 - 9, int_cards_graphics.size[1] + 20),
)
manager.add_set(
    col_cards_graphics[2],
    # Position on the screen of the entire set
    (width / 3 - 9, int_cards_graphics.size[1] + 20),
)
manager.add_set(
    col_cards_graphics[3],
    # Position on the screen of the entire set
    (5 * width / 12 - 12, int_cards_graphics.size[1] + 20),
)

card_back = AbstractCard("")
card_back.graphics_type = CardBackGraphics

pygame.display.flip()

clock = pygame.time.Clock()

stage = 0 # 0 = id face-up and rules face-down, 1 = everything face-down and shuffled

while 1: # game loop
    screen.fill("black")
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 0:
            index_list = [(i + 1) for i in range(len(int_cards))]
            random.shuffle(index_list)
            
            # flip the id cards face down and shuffle them
            for (i, card) in enumerate(int_cards):
                card.name = str(index_list[i])
                card.number = index_list[i]
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )

            # shuffle the columns (TODO: highlight that the columns shuffled)
            for (i, column) in enumerate(col_cards_graphics):
                for j in range(3):
                    column.append_card(col_cards_graphics[index_list[i] - 1].cardset[j])
            for column in col_cards_graphics:
                for j in range(3):
                    column.remove_card(column.cardset[0])
            
            stage = 1
            int_cards_graphics.clear_cache()
            for i in range(4):
                col_cards_graphics[i].clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 1:
            # flip the rule cards face up
            for (i, column) in enumerate(col_cards_graphics):
                for card in column.cardset:
                    card.face_up = True
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                    )
            stage = 2       
            int_cards_graphics.clear_cache()
            for i in range(4):
                col_cards_graphics[i].clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 2:
            index_list = [(i + 1) for i in range(len(int_cards))]
            random.shuffle(index_list)
            
            # flip the rule cards face down
            for (i, column) in enumerate(col_cards_graphics):
                for card in column.cardset:
                    card.face_up = False
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                    )
                    
            stage = 3
            int_cards_graphics.clear_cache()
            for i in range(4):
                col_cards_graphics[i].clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 3:
            # shuffle the id cards
            int_card_numbers = [card.number for card in int_cards]
            for (i, card) in enumerate(int_cards):
                card.name = str(int_card_numbers[index_list[i] - 1])
                card.number = int_card_numbers[index_list[i] - 1]
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
                
            # shuffle the columns
            for (i, column) in enumerate(col_cards_graphics):
                for j in range(3):
                    column.append_card(col_cards_graphics[index_list[i] - 1].cardset[j])
            for column in col_cards_graphics:
                for j in range(3):
                    column.remove_card(column.cardset[0])

            stage = 4
            int_cards_graphics.clear_cache()
            for i in range(4):
                col_cards_graphics[i].clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 4:
            # return rule cards to their original positions
            for (i, column) in enumerate(col_cards_graphics):
                for j in range(3):
                    col_cards_graphics[int_cards[i].number - 1].append_card(column.cardset[j])
            for column in col_cards_graphics:
                for j in range(3):
                    column.remove_card(column.cardset[0])
            
            # return id cards to (1, 2, 3, 4)
            for (i, card) in enumerate(int_cards):
                card.name = str(i + 1)
                card.number = i + 1
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
            
            int_cards_graphics.clear_cache()
            for i in range(4):
                col_cards_graphics[i].clear_cache()
    
        manager.process_events(event)

    manager.update(time_delta)
    manager.draw(screen)
    pygame.display.flip()
