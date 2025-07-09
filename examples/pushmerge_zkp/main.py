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

from suit_set import GRID_STATE, BB_CARDS, BD_CARDS, BE_CARDS, DB_CARDS, DD_CARDS, DE_CARDS, EB_CARDS, ED_CARDS, EE_CARDS, ABB_CARDSQ, AEB_CARDSQ, AED_CARDSQ, AEE_CARDSQ
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
removed_col_n = 0

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
            enc_cards_m_graphics.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 5:
            # place the id row of matrix Q
            id_cards_q = ID4Q
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
            encoding_1 = 3
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
            enc_cards_m_graphics.clear_cache()
            enc_cards_n_graphics.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 6:
            index_list = [(i + 1) for i in range(len(id_cards_n))]
            offset = random.randint(0, len(id_cards_n) - 1)
            for i in range(len(index_list)):
                index_list[i] = (index_list[i] + offset) % len(id_cards_n)
                if index_list[i] == 0:
                    index_list[i] = len(id_cards_n)
            
            # flip the id cards face down and shuffle them
            for (i, card) in enumerate(id_cards_n_graphics.cardset):
                card.name = str(index_list[i])
                card.number = index_list[i]
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )

            # shuffle the columns (TODO: highlight that the columns shuffled)
            for (i, column) in enumerate(col_cards_n_graphics):
                for j in range(2):
                    column.append_card(col_cards_n_graphics[index_list[i] - 1].cardset[j])
            for column in col_cards_n_graphics:
                for j in range(2):
                    column.remove_card(column.cardset[0])
                    
            # shuffle the encoding row
            for (i, card) in enumerate(enc_cards_n_graphics.cardset):
                if index_list[i] == encoding_1:
                    card.name = "1"
                    card.number = 1
                else:
                    card.name = "0"
                    card.number = 0

            stage = 7
            id_cards_m_graphics.clear_cache()
            id_cards_n_graphics.clear_cache()
            id_cards_q_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()
            enc_cards_m_graphics.clear_cache()
            enc_cards_n_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 7:
            # turn encoding row face-up
            for card in enc_cards_n_graphics.cardset:
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
            stage = 8
            enc_cards_n_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 8:
            # take the chosen column and move it to matrix Q
            grid_state_m_graphics.cardset[p_shuffled].name = "blank"
            grid_state_m_graphics.cardset[p_shuffled].graphics = SuitCardGraphics(
                grid_state_m_graphics.cardset[p_shuffled],
                filepath=Path("examples/pushmerge_zkp/images", "blank.png"),
            )
            col_cards_q = []
            for i in range(4):
                if enc_cards_n_graphics.cardset[i].name == "1":
                    removed_col_n = i
                    name0 = col_cards_n_graphics[i].cardset[0].name
                    name1 = col_cards_n_graphics[i].cardset[1].name
                    col_cards_n_graphics[i].cardset[0].name = "blank"
                    col_cards_n_graphics[i].cardset[0].graphics = SuitCardGraphics(
                        col_cards_n_graphics[i].cardset[0],
                        filepath=Path("examples/pushmerge_zkp/images", "blank.png"),
                    )
                    col_cards_n_graphics[i].cardset[1].name = "blank"
                    col_cards_n_graphics[i].cardset[1].graphics = SuitCardGraphics(
                        col_cards_n_graphics[i].cardset[1],
                        filepath=Path("examples/pushmerge_zkp/images", "blank.png"),
                    )
                    if name0 == "spade" and name1 == "spade":
                        col_cards_q.append(ABB_CARDSQ.copy())
                        col_cards_q.append(AEB_CARDSQ.copy())
                        col_cards_q.append(AED_CARDSQ.copy())
                        col_cards_q.append(AEE_CARDSQ.copy())
                    elif name0 == "club" and name1 == "spade":
                        col_cards_q.append(AEB_CARDSQ.copy())
                        col_cards_q.append(ABB_CARDSQ.copy())
                        col_cards_q.append(AED_CARDSQ.copy())
                        col_cards_q.append(AEE_CARDSQ.copy())
                    elif name0 == "club" and name1 == "diamond":
                        col_cards_q.append(AED_CARDSQ.copy())
                        col_cards_q.append(ABB_CARDSQ.copy())
                        col_cards_q.append(AEB_CARDSQ.copy())
                        col_cards_q.append(AEE_CARDSQ.copy())
                    else:
                        col_cards_q.append(AEE_CARDSQ.copy())
                        col_cards_q.append(ABB_CARDSQ.copy())
                        col_cards_q.append(AEB_CARDSQ.copy())
                        col_cards_q.append(AED_CARDSQ.copy())

            col_cards_q_graphics = [(AlignedHandVertical(
                                    col_cards_q[i],
                                    card_set_size_long,
                                    card_size=card_size,
                                    graphics_type=SuitCardGraphics,
                                )) for i in range(len(col_cards_q))]
            manager.add_set(
                col_cards_q_graphics[0],
                # Position on the screen of the entire set
                (width / 2, 5 * id_cards_n_graphics.size[1] + 10),
            )
            manager.add_set(
                col_cards_q_graphics[1],
                # Position on the screen of the entire set
                (width / 2 + width / 20 + 6, 5 * id_cards_n_graphics.size[1] + 10),
            )
            manager.add_set(
                col_cards_q_graphics[2],
                # Position on the screen of the entire set
                (width / 2 + width / 10 + 12, 5 * id_cards_n_graphics.size[1] + 10),
            )
            manager.add_set(
                col_cards_q_graphics[3],
                # Position on the screen of the entire set
                (width / 2 + width * 3 / 20 + 20, 5 * id_cards_n_graphics.size[1] + 10),
            )
            
            stage = 9
            id_cards_m_graphics.clear_cache()
            id_cards_n_graphics.clear_cache()
            id_cards_q_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()
            for column in col_cards_q_graphics:
                column.clear_cache()
            enc_cards_m_graphics.clear_cache()
            enc_cards_n_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 9:
            index_list = [(i + 1) for i in range(len(id_cards_q))]
            random.shuffle(index_list)
            # shuffle the id row of matrix Q and turn it face-down
            for (i, card) in enumerate(id_cards_q):
                card.name = str(index_list[i])
                card.number = index_list[i]
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
            
            # shuffle the columns of matrix Q
            for (i, column) in enumerate(col_cards_q_graphics):
                for j in range(3):
                    column.append_card(col_cards_q_graphics[index_list[i] - 1].cardset[j])
            for column in col_cards_q_graphics:
                for j in range(3):
                    column.remove_card(column.cardset[0])

            stage = 10
            id_cards_q_graphics.clear_cache()
            for column in col_cards_q_graphics:
                column.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 10:
            # turn the rule cards face-up
            for (i, column) in enumerate(col_cards_q_graphics):
                for card in column.cardset:
                    card.face_up = True
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                    )
            stage = 11
            for column in col_cards_q_graphics:
                column.clear_cache()
        
        # simulate all legal moves
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 11:
            for i in range(4):
                if col_cards_q_graphics[i].cardset[1].name == "spade" and col_cards_q_graphics[i].cardset[2].name == "spade":
                    col_cards_q_graphics[i].cardset[1].name = "club"
                    col_cards_q_graphics[i].cardset[1].graphics = SuitCardGraphics(
                        col_cards_q_graphics[i].cardset[1],
                        filepath=Path("examples/pushmerge_zkp/images", "club.png"),
                    )
                else:
                    col_cards_q_graphics[i].cardset[0].name = "club"
                    col_cards_q_graphics[i].cardset[0].graphics = SuitCardGraphics(
                        col_cards_q_graphics[i].cardset[0],
                        filepath=Path("examples/pushmerge_zkp/images", "club.png"),
                    )
                    col_cards_q_graphics[i].cardset[1].name = "heart"
                    col_cards_q_graphics[i].cardset[1].graphics = SuitCardGraphics(
                        col_cards_q_graphics[i].cardset[1],
                        filepath=Path("examples/pushmerge_zkp/images", "heart.png"),
                    )
            stage = 12
            for column in col_cards_q_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 12:
            index_list = [(i + 1) for i in range(len(id_cards_q))]
            random.shuffle(index_list)
            
            # flip the rule cards face down
            for (i, column) in enumerate(col_cards_q_graphics):
                for card in column.cardset:
                    card.face_up = False
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                    )
            
            stage = 13
            for column in col_cards_q_graphics:
                column.clear_cache()


        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 13:
            # shuffle the id cards
            int_card_numbers = [card.number for card in id_cards_q]
            for (i, card) in enumerate(id_cards_q_graphics.cardset):
                card.name = str(int_card_numbers[index_list[i] - 1])
                card.number = int_card_numbers[index_list[i] - 1]
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
                
            # shuffle the columns
            for (i, column) in enumerate(col_cards_q_graphics):
                for j in range(3):
                    column.append_card(col_cards_q_graphics[index_list[i] - 1].cardset[j])
            for column in col_cards_q_graphics:
                for j in range(3):
                    column.remove_card(column.cardset[0]) 
                      
            stage = 14
            id_cards_q_graphics.clear_cache()
            for column in col_cards_q_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 14:
            # return rule cards to their original positions
            for (i, column) in enumerate(col_cards_q_graphics):
                for j in range(3):
                    col_cards_q_graphics[id_cards_q[i].number - 1].append_card(column.cardset[j])
            for column in col_cards_q_graphics:
                for j in range(3):
                    column.remove_card(column.cardset[0])
            
            # return id cards to (1, 2, 3)
            for (i, card) in enumerate(id_cards_q):
                card.name = str(i + 1)
                card.number = i + 1
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
            
            stage = 15
            id_cards_q_graphics.clear_cache()
            for column in col_cards_q_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 15:
            # return the cards in column 1 of matrix Q to their original positions in matrix N
            col_cards_n_graphics[removed_col_n].remove_all_cards()
            col_cards_n_graphics[removed_col_n].append_card(
                col_cards_q_graphics[0].cardset[1]
            )
            col_cards_n_graphics[removed_col_n].append_card(
                col_cards_q_graphics[0].cardset[2]
            )

            # return the agent card to its original position in matrix M
            grid_state_m_graphics.cardset[p_shuffled].name = "heart"
            grid_state_m_graphics.cardset[p_shuffled].graphics = SuitCardGraphics(
                grid_state_m_graphics.cardset[p_shuffled],
                filepath=Path("examples/pushmerge_zkp/images", "heart.png"),
            )

            # discard matrix Q
            for i in range(4):
                id_cards_q_graphics.remove_card(id_cards_q_graphics.cardset[0])
            for column in col_cards_q_graphics:
                for j in range(3):
                    column.remove_card(column.cardset[0])
                    
            stage = 16
            id_cards_q_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 16:
            # discard the encoding row of matrix N
            for i in range(4):
                enc_cards_n_graphics.remove_card(enc_cards_n_graphics.cardset[0])
            
            # shuffle the id cards of N
            int_card_numbers = [card.number for card in id_cards_n]
            for (i, card) in enumerate(id_cards_n_graphics.cardset):
                card.name = str(int_card_numbers[index_list[i] - 1])
                card.number = int_card_numbers[index_list[i] - 1]
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                
            # shuffle the columns of N
            for (i, column) in enumerate(col_cards_n_graphics):
                for j in range(2):
                    column.append_card(col_cards_n_graphics[index_list[i] - 1].cardset[j])
            for column in col_cards_n_graphics:
                for j in range(2):
                    column.remove_card(column.cardset[0])

            stage = 17
            id_cards_n_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 17:
            # turn the id cards of N face-up
            for card in id_cards_n_graphics.cardset:
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
            stage = 18
            id_cards_n_graphics.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 18:
            # return rule cards to their original positions
            for (i, column) in enumerate(col_cards_n_graphics):
                for j in range(2):
                    col_cards_n_graphics[id_cards_n[i].number - 1].append_card(column.cardset[j])
            for column in col_cards_n_graphics:
                for j in range(2):
                    column.remove_card(column.cardset[0])
            
            # return id cards to (1, 2, 3, 4)
            for (i, card) in enumerate(id_cards_n):
                card.name = str(i + 1)
                card.number = i + 1
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
            
            stage = 19
            id_cards_n_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 19:
            p0 = [(p_shuffled - 5) % 20, (p_shuffled - 1) % 20, (p_shuffled + 1) % 20, (p_shuffled + 5) % 20]
            p1 = [(p_shuffled - 10) % 20, (p_shuffled - 2) % 20, (p_shuffled + 2) % 20, (p_shuffled + 10) % 20]
            # return the cards in column 1 of matrix N to their original positions in matrix M
            for i in range(4):
                grid_state_m_graphics.cardset[p0[i]].name = col_cards_n_graphics[i].cardset[0].name
                grid_state_m_graphics.cardset[p0[i]].face_up = False
                grid_state_m_graphics.cardset[p0[i]].graphics = SuitCardGraphics(
                    grid_state_m_graphics.cardset[p0[i]],
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                grid_state_m_graphics.cardset[p1[i]].name = col_cards_n_graphics[i].cardset[1].name
                grid_state_m_graphics.cardset[p1[i]].face_up = False
                grid_state_m_graphics.cardset[p1[i]].graphics = SuitCardGraphics(
                    grid_state_m_graphics.cardset[p1[i]],
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                
            # turn the agent card face-down
            grid_state_m_graphics.cardset[p_shuffled].face_up = False
            grid_state_m_graphics.cardset[p_shuffled].graphics = SuitCardGraphics(
                grid_state_m_graphics.cardset[p_shuffled],
                filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
            )
            
            # discard matrix N
            for i in range(4):
                id_cards_n_graphics.remove_card(id_cards_n_graphics.cardset[0])
            for column in col_cards_n_graphics:
                for j in range(2):
                    column.remove_card(column.cardset[0])
            stage = 20
            grid_state_m_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 20:
            # discard the encoding row of matrix M
            for i in range(20):
                enc_cards_m_graphics.remove_card(enc_cards_m_graphics.cardset[0])

            stage = 21
            id_cards_m_graphics.clear_cache()
            enc_cards_m_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 21:
            index_list = [(i + 1) for i in range(len(id_cards_m))]
            random.shuffle(index_list)
            
            # shuffle the id cards of M and turn them face-up
            int_card_numbers = [card.number for card in id_cards_m]
            for (i, card) in enumerate(id_cards_m_graphics.cardset):
                card.name = str(int_card_numbers[index_list[i] - 1])
                card.number = int_card_numbers[index_list[i] - 1]
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.number}.png"),
                )
                
            # shuffle the grid state of M
            grid_state_m_temp = []
            for i in range(len(grid_state_m)):
                grid_state_m_temp.append(grid_state_m[index_list[i] - 1])
            grid_state_m = grid_state_m_temp
            grid_state_m_graphics.cardset = grid_state_m_temp

            stage = 22
            id_cards_m_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 22:
            # return the grid state of M to its original positions
            grid_state_m_temp = [0 for _ in range(20)]
            for (i, card) in enumerate(grid_state_m_graphics.cardset):
                grid_state_m_temp[id_cards_m[i].number - 1] = card
            grid_state_m = grid_state_m_temp
            grid_state_m_graphics.cardset = grid_state_m_temp
            
            # return the id cards of M to (1, 2, ..., 20)
            for (i, card) in enumerate(id_cards_m):
                card.name = str(i + 1)
                card.number = i + 1
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
            
            stage = 23
            id_cards_m_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 23:
            for card in id_cards_m_graphics.cardset:
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                
            stage = 24
            id_cards_m_graphics.clear_cache()

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw(screen)
    pygame.display.flip()