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

from int_set import ID5, DUMMY_ONE, DUMMY_TWO, DUMMY_THREE, DUMMY_FOUR, DUMMY_FIVE, ENCODING
from pygame_cards.set import CardsSet

pygame.init()


screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
# screen = pygame.display.set_mode((400, 300))
size = width, height = screen.get_size()


manager = CardsManager()


# Creates your card set
id_cards = ID5.copy()
col_cards = [DUMMY_ONE.copy(), DUMMY_TWO.copy(), DUMMY_THREE.copy(), DUMMY_FOUR.copy(), DUMMY_FIVE.copy()] # col_cards[i] is the (i + 1)th column of cards
enc_cards = ENCODING.copy()

card_size = (width / 16, height / 8 - 10)
card_set_size_wide = (width / 3, height / 8)
card_set_size_long = (width / 15, height / 2)

id_cards_graphics = AlignedHand(
    id_cards,
    card_set_size_wide,
    card_size=card_size,
    graphics_type=IntCardGraphics,
)
manager.add_set(
    id_cards_graphics,
    # Position on the screen of the entire set
    (width / 6, 0),
)

col_cards_graphics = [(AlignedHandVertical(
                        col_cards[i],
                        card_set_size_long,
                        card_size=card_size,
                        graphics_type=SuitCardGraphics,
                    )) for i in range(len(col_cards))]
# Finally add the set to the manager
manager.add_set(
    col_cards_graphics[0],
    # Position on the screen of the entire set
    (width / 6 - 5, id_cards_graphics.size[1] + 10),
)
manager.add_set(
    col_cards_graphics[1],
    # Position on the screen of the entire set
    (width * 7 / 30, id_cards_graphics.size[1] + 10),
)
manager.add_set(
    col_cards_graphics[2],
    # Position on the screen of the entire set
    (width * 3 / 10 + 2, id_cards_graphics.size[1] + 10),
)
manager.add_set(
    col_cards_graphics[3],
    # Position on the screen of the entire set
    (width * 11 / 30 + 2, id_cards_graphics.size[1] + 10),
)
manager.add_set(
    col_cards_graphics[4],
    # Position on the screen of the entire set
    (width * 13 / 30 + 3, id_cards_graphics.size[1] + 10),
)

enc_cards_graphics = AlignedHand(
    enc_cards,
    card_set_size_wide,
    card_size=card_size,
    graphics_type=IntCardGraphics,
)

for card in enc_cards:
    card.graphics = IntCardGraphics(
        card,
        filepath=Path("examples/pushmerge_zkp/images", "blank.png"),
    )

manager.add_set(
    enc_cards_graphics,
    # Position on the screen of the entire set
    (width / 6, 5 * id_cards_graphics.size[1] + 15),
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
            # add encoding row
            for card in enc_cards:
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
            stage = 1
            enc_cards_graphics.clear_cache()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 1:
            index_list = [(i + 1) for i in range(len(id_cards))]
            offset = random.randint(0, len(id_cards) - 1)
            for i in range(len(index_list)):
                index_list[i] = (index_list[i] + offset) % len(id_cards)
                if index_list[i] == 0:
                    index_list[i] = len(id_cards)
            encoding_1 = 0
            
            # flip the id cards face down and shuffle them
            for (i, card) in enumerate(id_cards):
                if enc_cards_graphics.cardset[i].name == "1":
                    encoding_1 = card.number
                card.name = str(index_list[i])
                card.number = index_list[i]
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )

            # shuffle the columns (TODO: highlight that the columns shuffled)
            for (i, column) in enumerate(col_cards_graphics):
                for j in range(4):
                    column.append_card(col_cards_graphics[index_list[i] - 1].cardset[j])
            for column in col_cards_graphics:
                for j in range(4):
                    column.remove_card(column.cardset[0])
                    
            # shuffle the encoding row
            for (i, card) in enumerate(enc_cards):
                if index_list[i] == encoding_1:
                    card.name = "1"
                    card.number = 1
                else:
                    card.name = "0"
                    card.number = 0
            
            stage = 2
            id_cards_graphics.clear_cache()
            for i in range(len(col_cards_graphics)):
                col_cards_graphics[i].clear_cache()
            enc_cards_graphics.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 2:
            # flip the encoding row face up
            for (i, card) in enumerate(enc_cards):
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
            
            stage = 3
            id_cards_graphics.clear_cache()
            for i in range(len(col_cards_graphics)):
                col_cards_graphics[i].clear_cache()
            enc_cards_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 3:
            # remove chosen column from the matrix
            for (i, card) in enumerate(enc_cards):
                if card.name == "1":
                    for col_card in col_cards_graphics[i].cardset:
                        col_card.graphics = SuitCardGraphics(
                            col_card,
                            filepath=Path("examples/pushmerge_zkp/images", "blank.png"),
                        )
            stage = 4
            id_cards_graphics.clear_cache()
            for i in range(len(col_cards_graphics)):
                col_cards_graphics[i].clear_cache()
            enc_cards_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 4:
            # return chosen column to the matrix
            for (i, card) in enumerate(enc_cards):
                if card.name == "1":
                    for col_card in col_cards_graphics[i].cardset:
                        col_card.graphics = SuitCardGraphics(
                            col_card,
                            filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                        )
            stage = 5
            id_cards_graphics.clear_cache()
            for i in range(len(col_cards_graphics)):
                col_cards_graphics[i].clear_cache()
            enc_cards_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 5:
            # remove encoding row from the matrix
            for (i, card) in enumerate(enc_cards):
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "blank.png"),
                )
            stage = 6
            enc_cards_graphics.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 6:
            index_list = [(i + 1) for i in range(len(id_cards))]
            offset = random.randint(0, len(id_cards) - 1)
            for i in range(len(index_list)):
                index_list[i] = (index_list[i] + offset) % len(id_cards)
                if index_list[i] == 0:
                    index_list[i] = len(id_cards)
            
            # flip the encoding (and column) cards face down
            for (i, card) in enumerate(enc_cards):
                if card.name == "1":
                    for col_card in col_cards_graphics[i].cardset:
                        col_card.face_up = False
                        col_card.graphics = SuitCardGraphics(
                            col_card,
                            filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                        )
                # card.face_up = False
                # card.graphics = IntCardGraphics(
                #     card,
                #     filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                # )
            
            # shuffle the id cards
            encoding_1 = 0
            id_card_numbers = [card.number for card in id_cards]
            for (i, card) in enumerate(id_cards):
                if enc_cards_graphics.cardset[i].name == "1":
                    encoding_1 = id_card_numbers[i]
                card.name = str(id_card_numbers[index_list[i] - 1])
                card.number = id_card_numbers[index_list[i] - 1]
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
                
            # shuffle the columns
            for (i, column) in enumerate(col_cards_graphics):
                for j in range(4):
                    column.append_card(col_cards_graphics[index_list[i] - 1].cardset[j])
            for column in col_cards_graphics:
                for j in range(4):
                    column.remove_card(column.cardset[0])
                    
            # shuffle the encoding row
            # for (i, card) in enumerate(enc_cards):
            #     if id_cards[i].number == encoding_1:
            #         card.name = "1"
            #         card.number = 1
            #     else:
            #         card.name = "0"
            #         card.number = 0
                
            stage = 7
            id_cards_graphics.clear_cache()
            for i in range(len(col_cards_graphics)):
                col_cards_graphics[i].clear_cache()
            enc_cards_graphics.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 7:
            # return rule cards to their original positions
            for (i, column) in enumerate(col_cards_graphics):
                for j in range(4):
                    col_cards_graphics[id_cards[i].number - 1].append_card(column.cardset[j])
            for column in col_cards_graphics:
                for j in range(4):
                    column.remove_card(column.cardset[0])
            
            # return id cards to their original positions
            encoding_1 = 0
            for (i, card) in enumerate(id_cards):
                if enc_cards_graphics.cardset[i].name == "1":
                    encoding_1 = card.number
                card.name = str(i + 1)
                card.number = i + 1
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
                
            # return encoding row to its original positions
            # for (i, card) in enumerate(enc_cards):
            #     if id_cards[i].number == encoding_1:
            #         card.name = "1"
            #         card.number = 1
            #     else:
            #         card.name = "0"
            #         card.number = 0

            id_cards_graphics.clear_cache()
            for i in range(3):
                col_cards_graphics[i].clear_cache()
            enc_cards_graphics.clear_cache()
    
        manager.process_events(event)

    manager.update(time_delta)
    manager.draw(screen)
    pygame.display.flip()
