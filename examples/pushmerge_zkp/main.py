import random
import sys
import copy
import pygame
from pathlib import Path
from suit_card import SuitCard
from suit_card_graphics import SuitCardGraphics
from int_card_graphics import IntCardGraphics
from pygame_cards.abstract import AbstractCard
from pygame_cards.back import CardBackGraphics
from pygame_cards.hands import AlignedHand, AlignedHandVertical
from pygame_cards.manager import CardSetRights, CardsManager

from suit_set import GRID_STATE, BB_CARDS, BD_CARDS, BE_CARDS, DB_CARDS, DD_CARDS, DE_CARDS, EB_CARDS, ED_CARDS, EE_CARDS
from int_set import ID4, ID4Q, ID20, ENCODING_MOVE_1, ENCODING_3_LENGTH_4
from pygame_cards.set import CardsSet

pygame.init()


screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
# screen = pygame.display.set_mode((400, 300))
size = width, height = screen.get_size()


manager = CardsManager()


# Creates your card set
id_cards_m = ID20
grid_state_m = GRID_STATE

card_size = (width / 21, height / 9 - 10)
card_set_size_wide = (width - 10, height / 9)
card_set_size_long = (width / 21, height / 2)

id_cards_m_graphics = AlignedHand(
    id_cards_m,
    card_set_size_wide,
    card_size=card_size,
    graphics_type=IntCardGraphics,
)
manager.add_set(
    id_cards_m_graphics,
    (0, 0),
)
grid_state_m_graphics = AlignedHand(
        grid_state_m,
        card_set_size_wide,
        card_size=card_size,
        graphics_type=SuitCardGraphics,
)

manager.add_set(
    grid_state_m_graphics,
    # Position on the screen of the entire set
    (0, id_cards_m_graphics.size[1] + 5),
)

card_back = AbstractCard("")
card_back.graphics_type = CardBackGraphics

pygame.display.flip()

clock = pygame.time.Clock()

stage = 0 # 0 = everything in M face-up, 1 = everything in M face-down, 2 = add encoder row for chosen pile cut

encoding_1 = 0

p_shuffled = 0

while 1: # game loop
    screen.fill("black")
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 0:
            for card in id_cards_m_graphics.cardset:
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
            for card in grid_state_m_graphics.cardset:
                card.face_up = False
                card.graphics = SuitCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
            stage = 1
            id_cards_m_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 1:
            # add encoding row for chosen pile cut
            enc_cards_m = ENCODING_MOVE_1
            enc_cards_m_graphics = AlignedHand(
                enc_cards_m,
                card_set_size_wide,
                card_size=card_size,
                graphics_type=IntCardGraphics,
            )
            manager.add_set(
                enc_cards_m_graphics,
                # Position on the screen of the entire set
                (0, 2 * grid_state_m_graphics.size[1] + 10),
            )
            
            # generate random pile shifting shuffle
            index_list = [(i + 1) for i in range(len(id_cards_m))]
            offset = random.randint(0, len(id_cards_m) - 1)
            for i in range(len(index_list)):
                index_list[i] = (index_list[i] + offset) % len(id_cards_m)
                if index_list[i] == 0:
                    index_list[i] = len(id_cards_m)
            
            # flip the id cards face down and shuffle them
            for (i, card) in enumerate(id_cards_m):
                if enc_cards_m_graphics.cardset[i].name == "1":
                    encoding_1 = card.number
                card.name = str(index_list[i])
                card.number = index_list[i]

            # shuffle the columns
            grid_state_m_temp = []
            for i in range(len(grid_state_m)):
                grid_state_m_temp.append(grid_state_m[index_list[i] - 1])
            grid_state_m = grid_state_m_temp
            grid_state_m_graphics.cardset = grid_state_m_temp
                    
            # shuffle the encoding row
            for (i, card) in enumerate(enc_cards_m):
                if index_list[i] == encoding_1:
                    card.name = "1"
                    card.number = 1
                else:
                    card.name = "0"
                    card.number = 0
            stage = 2
            id_cards_m_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            enc_cards_m_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 2:
            # turn the encoding row face up
            for card in enc_cards_m_graphics.cardset:
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
            stage = 3
            enc_cards_m_graphics.clear_cache()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 3:
            # turn the chosen card face-up
            for i in range(len(enc_cards_m_graphics.cardset)):
                if enc_cards_m_graphics.cardset[i].name == "1":
                    p_shuffled = i
                    grid_state_m_graphics.cardset[i].face_up = True
                    grid_state_m_graphics.cardset[i].graphics = SuitCardGraphics(
                        grid_state_m_graphics.cardset[i],
                        filepath=Path("examples/pushmerge_zkp/images", f"{grid_state_m_graphics.cardset[i].name}.png"),
                    )
            stage = 4
            grid_state_m_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 4:
            # place the id row of matrix N
            id_cards_n = ID4
            id_cards_n_graphics = AlignedHand(
                id_cards_n,
                card_set_size_wide,
                card_size=card_size,
                graphics_type=IntCardGraphics,
            )
            manager.add_set(
                id_cards_n_graphics,
                (0, 4 * grid_state_m_graphics.size[1]),
            )

            # place the second and third rows of matrix N
            col_cards_n = []
            p0 = [(p_shuffled - 5) % 20, (p_shuffled - 1) % 20, (p_shuffled + 1) % 20, (p_shuffled + 5) % 20]
            p1 = [(p_shuffled - 10) % 20, (p_shuffled - 2) % 20, (p_shuffled + 2) % 20, (p_shuffled + 10) % 20]

            for i in range(4):
                if grid_state_m_graphics.cardset[p0[i]].name == "spade" and grid_state_m_graphics.cardset[p1[i]].name == "spade":
                    col_cards_n.append(BB_CARDS.copy())
                elif grid_state_m_graphics.cardset[p0[i]].name == "spade" and grid_state_m_graphics.cardset[p1[i]].name == "diamond":
                    col_cards_n.append(BD_CARDS.copy())
                elif grid_state_m_graphics.cardset[p0[i]].name == "spade" and grid_state_m_graphics.cardset[p1[i]].name == "club":
                    col_cards_n.append(BE_CARDS.copy())
                elif grid_state_m_graphics.cardset[p0[i]].name == "diamond" and grid_state_m_graphics.cardset[p1[i]].name == "spade":
                    col_cards_n.append(DB_CARDS.copy())
                elif grid_state_m_graphics.cardset[p0[i]].name == "diamond" and grid_state_m_graphics.cardset[p1[i]].name == "diamond":
                    col_cards_n.append(DD_CARDS.copy())
                elif grid_state_m_graphics.cardset[p0[i]].name == "diamond" and grid_state_m_graphics.cardset[p1[i]].name == "club":
                    col_cards_n.append(DE_CARDS.copy())
                elif grid_state_m_graphics.cardset[p0[i]].name == "club" and grid_state_m_graphics.cardset[p1[i]].name == "spade":
                    col_cards_n.append(EB_CARDS.copy())
                elif grid_state_m_graphics.cardset[p0[i]].name == "club" and grid_state_m_graphics.cardset[p1[i]].name == "diamond":
                    col_cards_n.append(ED_CARDS.copy())
                else:
                    col_cards_n.append(EE_CARDS.copy())
                    
                col_cards_n_graphics = [(AlignedHandVertical(
                                        col_cards_n[i],
                                        card_set_size_long,
                                        card_size=card_size,
                                        graphics_type=SuitCardGraphics,
                                    )) for i in range(len(col_cards_n))]
            manager.add_set(
                col_cards_n_graphics[0],
                # Position on the screen of the entire set
                (0, 5 * id_cards_n_graphics.size[1] + 10),
            )
            manager.add_set(
                col_cards_n_graphics[1],
                # Position on the screen of the entire set
                (width / 20 + 6, 5 * id_cards_n_graphics.size[1] + 10),
            )
            manager.add_set(
                col_cards_n_graphics[2],
                # Position on the screen of the entire set
                (width / 10 + 12, 5 * id_cards_n_graphics.size[1] + 10),
            )
            manager.add_set(
                col_cards_n_graphics[3],
                # Position on the screen of the entire set
                (width * 3 / 20 + 20, 5 * id_cards_n_graphics.size[1] + 10),
            )
            
            for i in range(4):
                grid_state_m_graphics.cardset[p0[i]].name = "blank"
                grid_state_m_graphics.cardset[p1[i]].name = "blank"
                grid_state_m_graphics.cardset[p0[i]].graphics = SuitCardGraphics(
                    grid_state_m_graphics.cardset[p0[i]],
                    filepath=Path("examples/pushmerge_zkp/images", "blank.png"),
                )
                grid_state_m_graphics.cardset[p1[i]].graphics = SuitCardGraphics(
                    grid_state_m_graphics.cardset[p1[i]],
                    filepath=Path("examples/pushmerge_zkp/images", "blank.png"),
                )
            
            stage = 5
            id_cards_m_graphics.clear_cache()
            id_cards_n_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 5:
            # place the id row of matrix Q
            id_cards_q = ID4
            id_cards_q_graphics = AlignedHand(
                id_cards_q,
                card_set_size_wide,
                card_size=card_size,
                graphics_type=IntCardGraphics,
            )
            manager.add_set(
                id_cards_q_graphics,
                (width / 2, 4 * grid_state_m_graphics.size[1]),
            )
            
            # place an encoding row under matrix N for the chosen pile cut
            enc_cards_n = ENCODING_3_LENGTH_4
            enc_cards_n_graphics = AlignedHand(
                enc_cards_n,
                card_set_size_wide,
                card_size=card_size,
                graphics_type=IntCardGraphics,
            )
            manager.add_set(
                enc_cards_n_graphics,
                (0, 7 * grid_state_m_graphics.size[1] + 10),
            )
            
            stage = 6
            id_cards_m_graphics.clear_cache()
            id_cards_n_graphics.clear_cache()
            id_cards_q_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()
                    

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw(screen)
    pygame.display.flip()