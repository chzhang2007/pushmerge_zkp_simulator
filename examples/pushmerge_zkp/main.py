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

from suit_set import GRID_STATE, BB_CARDS, BB_CARDS2, BB_CARDS3, BB_CARDS4, BD_CARDS, BD_CARDS2, BD_CARDS3, BD_CARDS4, BE_CARDS, BE_CARDS2, BE_CARDS3, BE_CARDS4, DB_CARDS, DB_CARDS2, DB_CARDS3, DB_CARDS4, DD_CARDS, DD_CARDS2, DD_CARDS3, DD_CARDS4, DE_CARDS, DE_CARDS2, DE_CARDS3, DE_CARDS4, EB_CARDS, EB_CARDS2, EB_CARDS3, EB_CARDS4, ED_CARDS, ED_CARDS2, ED_CARDS3, ED_CARDS4, EE_CARDS, EE_CARDS2, EE_CARDS3, EE_CARDS4, ABB_CARDSQ, AEB_CARDSQ, AED_CARDSQ, AEE_CARDSQ
from int_set import ID4, ID4Q, ID20, ENCODING_MOVE_1, ENCODING_MOVE_2, ENCODING_MOVE_3, ENCODING_MOVE_4, ENCODING_1_LENGTH_4, ENCODING_2_LENGTH_4, ENCODING_3_LENGTH_4, ENCODING_4_LENGTH_4
from pygame_cards.set import CardsSet

pygame.init()


screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
size = width, height = screen.get_size()


manager = CardsManager()

id_cards_m = ID20


# TO CHANGE INPUT: MODIFY HERE (INPUTS RESTRICTED TO A 2x3 GRID)
grid_state_m = GRID_STATE # initial grid state
number_of_moves = 4
# to modify encoding_rows_m, go into int_set.py and modify the sets ENCODING_MOVE_1, ENCODING_MOVE_2, etc.
encoding_rows_m = [ENCODING_MOVE_1.copy(), ENCODING_MOVE_2.copy(), ENCODING_MOVE_3.copy(), ENCODING_MOVE_4.copy()]
# to modify encoding_rows_n, simply modify this array
encoding_rows_n = [ENCODING_3_LENGTH_4.copy(), ENCODING_3_LENGTH_4.copy(), ENCODING_1_LENGTH_4.copy(), ENCODING_3_LENGTH_4.copy()]
# modify encoding_1_m and encoding_1_n (1-indexed) to match encoding_rows_m and encoding_rows_n
encoding_1_m = [12, 12, 13, 8]
encoding_1_n = [3, 3, 1, 3]
# modify the target position (1-indexed) to match the Push Merge instance
target_pos = 9
# if tutorial, face-down cards will be visible
tutorial = True

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

bb_cards = [BB_CARDS.copy(), BB_CARDS2.copy(), BB_CARDS3.copy(), BB_CARDS4.copy()]
bd_cards = [BD_CARDS.copy(), BD_CARDS2.copy(), BD_CARDS3.copy(), BD_CARDS4.copy()]
be_cards = [BE_CARDS.copy(), BE_CARDS2.copy(), BE_CARDS3.copy(), BE_CARDS4.copy()]
db_cards = [DB_CARDS.copy(), DB_CARDS2.copy(), DB_CARDS3.copy(), DB_CARDS4.copy()]
dd_cards = [DD_CARDS.copy(), DD_CARDS2.copy(), DD_CARDS3.copy(), DD_CARDS4.copy()]
de_cards = [DE_CARDS.copy(), DE_CARDS2.copy(), DE_CARDS3.copy(), DE_CARDS4.copy()]
eb_cards = [EB_CARDS.copy(), EB_CARDS2.copy(), EB_CARDS3.copy(), EB_CARDS4.copy()]
ed_cards = [ED_CARDS.copy(), ED_CARDS2.copy(), ED_CARDS3.copy(), ED_CARDS4.copy()]
ee_cards = [EE_CARDS.copy(), EE_CARDS2.copy(), EE_CARDS3.copy(), EE_CARDS4.copy()]

pygame.display.flip()

clock = pygame.time.Clock()

stage = -1

p_shuffled = 0
removed_col_n = 0
current_move = 0

while 1: # game loop
    screen.fill("black")
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == -1 and current_move < number_of_moves:
            for card in id_cards_m_graphics.cardset:
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            for card in grid_state_m_graphics.cardset:
                card.face_up = False
                card.graphics = SuitCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            stage = 0
            id_cards_m_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and current_move >= number_of_moves:
            if current_move == number_of_moves:
                # turn the card at the target position face-up to ensure it is the agent
                grid_state_m_graphics.cardset[target_pos - 1].face_up = True
                grid_state_m_graphics.cardset[target_pos - 1].graphics = SuitCardGraphics(
                    grid_state_m_graphics.cardset[target_pos - 1],
                    filepath=Path("examples/pushmerge_zkp/images", f"{grid_state_m_graphics.cardset[target_pos - 1].name}.png"),
                )
                current_move += 1
                grid_state_m_graphics.clear_cache()
            
        # START OF MOVE CHECK
        
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 0:
            # add encoding row for chosen pile cut
            enc_cards_m = encoding_rows_m[current_move].copy()
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
            if tutorial:
                for (i, card) in enumerate(enc_cards_m_graphics.cardset):
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
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
                card.name = str(index_list[i])
                card.number = index_list[i]
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )

            # shuffle the columns
            grid_state_m_temp = []
            for i in range(len(grid_state_m)):
                grid_state_m_temp.append(grid_state_m[index_list[i] - 1])
            grid_state_m = grid_state_m_temp
            grid_state_m_graphics.cardset = grid_state_m_temp
                    
            # shuffle the encoding row
            for (i, card) in enumerate(enc_cards_m):
                if index_list[i] == encoding_1_m[current_move]:
                    card.name = "1"
                    card.number = 1
                else:
                    card.name = "0"
                    card.number = 0
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            stage = 1
            id_cards_m_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            enc_cards_m_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 1:
            # turn the encoding row face up
            for card in enc_cards_m_graphics.cardset:
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
            stage = 2
            enc_cards_m_graphics.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 2:
            # turn the chosen card face-up
            for i in range(len(enc_cards_m_graphics.cardset)):
                if enc_cards_m_graphics.cardset[i].name == "1":
                    p_shuffled = i
                    grid_state_m_graphics.cardset[i].face_up = True
                    grid_state_m_graphics.cardset[i].graphics = SuitCardGraphics(
                        grid_state_m_graphics.cardset[i],
                        filepath=Path("examples/pushmerge_zkp/images", f"{grid_state_m_graphics.cardset[i].name}.png"),
                    )
            stage = 3
            grid_state_m_graphics.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 3:
            # place the id row of matrix N
            id_cards_n = ID4.copy()
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
            if tutorial:
                for (i, card) in enumerate(id_cards_n_graphics.cardset):
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )

            # place the second and third rows of matrix N
            col_cards_n = []
            p0 = [(p_shuffled - 5) % 20, (p_shuffled - 1) % 20, (p_shuffled + 1) % 20, (p_shuffled + 5) % 20]
            p1 = [(p_shuffled - 10) % 20, (p_shuffled - 2) % 20, (p_shuffled + 2) % 20, (p_shuffled + 10) % 20]

            bb_index = 0
            bd_index = 0
            be_index = 0
            db_index = 0
            dd_index = 0
            de_index = 0
            eb_index = 0
            ed_index = 0
            ee_index = 0
            for i in range(4):
                if grid_state_m_graphics.cardset[p0[i]].name == "spade" and grid_state_m_graphics.cardset[p1[i]].name == "spade":
                    col_cards_n.append(bb_cards[bb_index].copy())
                    bb_index += 1
                elif grid_state_m_graphics.cardset[p0[i]].name == "spade" and grid_state_m_graphics.cardset[p1[i]].name == "diamond":
                    col_cards_n.append(bd_cards[bd_index].copy())
                    bd_index += 1
                elif grid_state_m_graphics.cardset[p0[i]].name == "spade" and grid_state_m_graphics.cardset[p1[i]].name == "club":
                    col_cards_n.append(be_cards[be_index].copy())
                    be_index += 1
                elif grid_state_m_graphics.cardset[p0[i]].name == "diamond" and grid_state_m_graphics.cardset[p1[i]].name == "spade":
                    col_cards_n.append(db_cards[db_index].copy())
                    db_index += 1
                elif grid_state_m_graphics.cardset[p0[i]].name == "diamond" and grid_state_m_graphics.cardset[p1[i]].name == "diamond":
                    col_cards_n.append(dd_cards[dd_index].copy())
                    dd_index += 1
                elif grid_state_m_graphics.cardset[p0[i]].name == "diamond" and grid_state_m_graphics.cardset[p1[i]].name == "club":
                    col_cards_n.append(de_cards[de_index].copy())
                    de_index += 1
                elif grid_state_m_graphics.cardset[p0[i]].name == "club" and grid_state_m_graphics.cardset[p1[i]].name == "spade":
                    col_cards_n.append(eb_cards[eb_index].copy())
                    eb_index += 1
                elif grid_state_m_graphics.cardset[p0[i]].name == "club" and grid_state_m_graphics.cardset[p1[i]].name == "diamond":
                    col_cards_n.append(ed_cards[ed_index].copy())
                    ed_index += 1
                else:
                    col_cards_n.append(ee_cards[ee_index].copy())
                    ee_index += 1

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
            if tutorial:
                for (i, card) in enumerate(col_cards_n_graphics[0].cardset):
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            manager.add_set(
                col_cards_n_graphics[1],
                # Position on the screen of the entire set
                (width / 20 + 6, 5 * id_cards_n_graphics.size[1] + 10),
            )
            if tutorial:
                for (i, card) in enumerate(col_cards_n_graphics[1].cardset):
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            manager.add_set(
                col_cards_n_graphics[2],
                # Position on the screen of the entire set
                (width / 10 + 12, 5 * id_cards_n_graphics.size[1] + 10),
            )
            if tutorial:
                for (i, card) in enumerate(col_cards_n_graphics[2].cardset):
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            manager.add_set(
                col_cards_n_graphics[3],
                # Position on the screen of the entire set
                (width * 3 / 20 + 20, 5 * id_cards_n_graphics.size[1] + 10),
            )
            if tutorial:
                for (i, card) in enumerate(col_cards_n_graphics[3].cardset):
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
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

            stage = 4
            id_cards_m_graphics.clear_cache()
            id_cards_n_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()
            enc_cards_m_graphics.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 4:
            # place the id row of matrix Q
            id_cards_q = ID4Q.copy()
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
            if tutorial:
                for (i, card) in enumerate(id_cards_q_graphics.cardset):
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )

            # place an encoding row under matrix N for the chosen pile cut
            enc_cards_n = encoding_rows_n[current_move].copy()
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
            if tutorial:
                for (i, card) in enumerate(enc_cards_n_graphics.cardset):
                    card.face_up = False
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            for (i, card) in enumerate(enc_cards_n_graphics.cardset):
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )

            stage = 5
            id_cards_m_graphics.clear_cache()
            id_cards_n_graphics.clear_cache()
            id_cards_q_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()
            enc_cards_m_graphics.clear_cache()
            enc_cards_n_graphics.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 5:
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
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
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
                if index_list[i] == encoding_1_n[current_move]:
                    card.name = "1"
                    card.number = 1
                else:
                    card.name = "0"
                    card.number = 0
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
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
            # turn encoding row face-up
            for card in enc_cards_n_graphics.cardset:
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
            stage = 7
            enc_cards_n_graphics.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 7:
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
            if tutorial:
                for (i, card) in enumerate(col_cards_q_graphics[0].cardset):
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            manager.add_set(
                col_cards_q_graphics[1],
                # Position on the screen of the entire set
                (width / 2 + width / 20 + 6, 5 * id_cards_n_graphics.size[1] + 10),
            )
            if tutorial:
                for (i, card) in enumerate(col_cards_q_graphics[1].cardset):
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            manager.add_set(
                col_cards_q_graphics[2],
                # Position on the screen of the entire set
                (width / 2 + width / 10 + 12, 5 * id_cards_n_graphics.size[1] + 10),
            )
            if tutorial:
                for (i, card) in enumerate(col_cards_q_graphics[2].cardset):
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            manager.add_set(
                col_cards_q_graphics[3],
                # Position on the screen of the entire set
                (width / 2 + width * 3 / 20 + 20, 5 * id_cards_n_graphics.size[1] + 10),
            )
            if tutorial:
                for (i, card) in enumerate(col_cards_q_graphics[3].cardset):
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )

            stage = 8
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

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 8:
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
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            
            # shuffle the columns of matrix Q
            for (i, column) in enumerate(col_cards_q_graphics):
                for j in range(3):
                    column.append_card(col_cards_q_graphics[index_list[i] - 1].cardset[j])
            for column in col_cards_q_graphics:
                for j in range(3):
                    column.remove_card(column.cardset[0])

            stage = 9
            id_cards_q_graphics.clear_cache()
            for column in col_cards_q_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 9:
            # turn the rule cards face-up
            for (i, column) in enumerate(col_cards_q_graphics):
                for card in column.cardset:
                    card.face_up = True
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                    )
            stage = 10
            for column in col_cards_q_graphics:
                column.clear_cache()
        
        # simulate all legal moves
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 10:
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
            stage = 11
            for column in col_cards_q_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 11:
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
                    if tutorial:
                        card.graphics = SuitCardGraphics(
                            card,
                            filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                        )
            
            stage = 12
            for column in col_cards_q_graphics:
                column.clear_cache()


        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 12:
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
                      
            stage = 13
            id_cards_q_graphics.clear_cache()
            for column in col_cards_q_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 13:
            # return rule cards to their original positions
            for (i, column) in enumerate(col_cards_q_graphics):
                for j in range(3):
                    col_cards_q_graphics[id_cards_q[i].number - 1].append_card(column.cardset[j])
            for column in col_cards_q_graphics:
                for j in range(3):
                    column.remove_card(column.cardset[0])
            
            # return id cards to (1, 2, 3, 4)
            for (i, card) in enumerate(id_cards_q):
                card.name = str(i + 1)
                card.number = i + 1
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
            
            stage = 14
            id_cards_q_graphics.clear_cache()
            for column in col_cards_q_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 14:
            # return the cards in column 1 of matrix Q to their original positions in matrix N
            col_cards_n_graphics[removed_col_n].remove_all_cards()
            col_cards_n_graphics[removed_col_n].append_card(
                col_cards_q_graphics[0].cardset[1]
            )
            col_cards_n_graphics[removed_col_n].append_card(
                col_cards_q_graphics[0].cardset[2]
            )

            # return q[0][0] to the agent's original position in matrix M
            grid_state_m_graphics.cardset[p_shuffled].name = col_cards_q_graphics[0].cardset[0].name
            grid_state_m_graphics.cardset[p_shuffled].face_up = False
            grid_state_m_graphics.cardset[p_shuffled].graphics = SuitCardGraphics(
                grid_state_m_graphics.cardset[p_shuffled],
                filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
            )
            if tutorial:
                grid_state_m_graphics.cardset[p_shuffled].graphics = SuitCardGraphics(
                    grid_state_m_graphics.cardset[p_shuffled],
                    filepath=Path("examples/pushmerge_zkp/images", f"{grid_state_m_graphics.cardset[p_shuffled].name}_tutorial.png"),
                )

            # discard matrix Q
            for i in range(4):
                id_cards_q_graphics.remove_card(id_cards_q_graphics.cardset[0])
            for column in col_cards_q_graphics:
                for j in range(3):
                    column.remove_card(column.cardset[0])

            stage = 15
            id_cards_q_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 15:
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
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )

            # shuffle the columns of N
            for (i, column) in enumerate(col_cards_n_graphics):
                for j in range(2):
                    column.append_card(col_cards_n_graphics[index_list[i] - 1].cardset[j])
            for column in col_cards_n_graphics:
                for j in range(2):
                    column.remove_card(column.cardset[0])

            stage = 16
            id_cards_n_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 16:
            # turn the id cards of N face-up
            for card in id_cards_n_graphics.cardset:
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", f"{card.name}.png"),
                )
            stage = 17
            id_cards_n_graphics.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 17:
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

            stage = 18
            id_cards_n_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 18:
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
                if tutorial:
                    grid_state_m_graphics.cardset[p0[i]].graphics = SuitCardGraphics(
                        grid_state_m_graphics.cardset[p0[i]],
                        filepath=Path("examples/pushmerge_zkp/images", f"{grid_state_m_graphics.cardset[p0[i]].name}_tutorial.png"),
                    )
                grid_state_m_graphics.cardset[p1[i]].name = col_cards_n_graphics[i].cardset[1].name
                grid_state_m_graphics.cardset[p1[i]].face_up = False
                grid_state_m_graphics.cardset[p1[i]].graphics = SuitCardGraphics(
                    grid_state_m_graphics.cardset[p1[i]],
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    grid_state_m_graphics.cardset[p1[i]].graphics = SuitCardGraphics(
                        grid_state_m_graphics.cardset[p1[i]],
                        filepath=Path("examples/pushmerge_zkp/images", f"{grid_state_m_graphics.cardset[p1[i]].name}_tutorial.png"),
                    )
            
            # discard matrix N
            for i in range(4):
                id_cards_n_graphics.remove_card(id_cards_n_graphics.cardset[0])
            for column in col_cards_n_graphics:
                for j in range(2):
                    column.remove_card(column.cardset[0])
            stage = 19
            grid_state_m_graphics.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 19:
            # discard the encoding row of matrix M
            for i in range(20):
                enc_cards_m_graphics.remove_card(enc_cards_m_graphics.cardset[0])

            stage = 20
            id_cards_m_graphics.clear_cache()
            enc_cards_m_graphics.clear_cache()
            for column in col_cards_n_graphics:
                column.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 20:
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
            if tutorial:
                for (i, card) in enumerate(grid_state_m_graphics.cardset):
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )

            stage = 21
            id_cards_m_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 21:
            # return the grid state of M to its original positions
            grid_state_m_temp = [0 for _ in range(20)]
            for (i, card) in enumerate(grid_state_m_graphics.cardset):
                grid_state_m_temp[id_cards_m[i].number - 1] = card
                if tutorial:
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
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
            
            stage = 22
            id_cards_m_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 22:
            for card in id_cards_m_graphics.cardset:
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
                
            stage = 0
            current_move += 1
            id_cards_m_graphics.clear_cache()
            
            for i in range(4):
                bb_cards[i][0].name = "spade"
                bb_cards[i][1].name = "spade"
                bd_cards[i][0].name = "spade"
                bd_cards[i][1].name = "diamond"
                be_cards[i][0].name = "spade"
                be_cards[i][1].name = "club"
                db_cards[i][0].name = "diamond"
                db_cards[i][1].name = "spade"
                dd_cards[i][0].name = "diamond"
                dd_cards[i][1].name = "diamond"
                de_cards[i][0].name = "diamond"
                de_cards[i][1].name = "club"
                eb_cards[i][0].name = "club"
                eb_cards[i][1].name = "spade"
                ed_cards[i][0].name = "club"
                ed_cards[i][1].name = "diamond"
                ee_cards[i][0].name = "club"
                ee_cards[i][1].name = "club"
                for j in range(2):
                    bb_cards[i][j].face_up = False
                    bb_cards[i][j].graphics = SuitCardGraphics(
                        bb_cards[i][j],
                        filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                    )
                    if tutorial:
                        bb_cards[i][j].graphics = SuitCardGraphics(
                            bb_cards[i][j],
                            filepath=Path("examples/pushmerge_zkp/images", f"{bb_cards[i][j].name}_tutorial.png"),
                        )
                    bd_cards[i][j].face_up = False
                    bd_cards[i][j].graphics = SuitCardGraphics(
                        bd_cards[i][j],
                        filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                    )
                    if tutorial:
                        bd_cards[i][j].graphics = SuitCardGraphics(
                            bd_cards[i][j],
                            filepath=Path("examples/pushmerge_zkp/images", f"{bd_cards[i][j].name}_tutorial.png"),
                        )
                    be_cards[i][j].face_up = False
                    be_cards[i][j].graphics = SuitCardGraphics(
                        be_cards[i][j],
                        filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                    )
                    if tutorial:
                        be_cards[i][j].graphics = SuitCardGraphics(
                            be_cards[i][j],
                            filepath=Path("examples/pushmerge_zkp/images", f"{be_cards[i][j].name}_tutorial.png"),
                        )
                    db_cards[i][j].face_up = False
                    db_cards[i][j].graphics = SuitCardGraphics(
                        db_cards[i][j],
                        filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                    )
                    if tutorial:
                        db_cards[i][j].graphics = SuitCardGraphics(
                            db_cards[i][j],
                            filepath=Path("examples/pushmerge_zkp/images", f"{db_cards[i][j].name}_tutorial.png"),
                        )
                    dd_cards[i][j].face_up = False
                    dd_cards[i][j].graphics = SuitCardGraphics(
                        dd_cards[i][j],
                        filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                    )
                    if tutorial:
                        dd_cards[i][j].graphics = SuitCardGraphics(
                            dd_cards[i][j],
                            filepath=Path("examples/pushmerge_zkp/images", f"{dd_cards[i][j].name}_tutorial.png"),
                        )
                    de_cards[i][j].face_up = False
                    de_cards[i][j].graphics = SuitCardGraphics(
                        de_cards[i][j],
                        filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                    )
                    if tutorial:
                        de_cards[i][j].graphics = SuitCardGraphics(
                            de_cards[i][j],
                            filepath=Path("examples/pushmerge_zkp/images", f"{de_cards[i][j].name}_tutorial.png"),
                        )
                    eb_cards[i][j].face_up = False
                    eb_cards[i][j].graphics = SuitCardGraphics(
                        eb_cards[i][j],
                        filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                    )
                    if tutorial:
                        eb_cards[i][j].graphics = SuitCardGraphics(
                            eb_cards[i][j],
                            filepath=Path("examples/pushmerge_zkp/images", f"{eb_cards[i][j].name}_tutorial.png"),
                        )
                    ed_cards[i][j].face_up = False
                    ed_cards[i][j].graphics = SuitCardGraphics(
                        ed_cards[i][j],
                        filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                    )
                    if tutorial:
                        ed_cards[i][j].graphics = SuitCardGraphics(
                            ed_cards[i][j],
                            filepath=Path("examples/pushmerge_zkp/images", f"{ed_cards[i][j].name}_tutorial.png"),
                        )
                    ee_cards[i][j].face_up = False
                    ee_cards[i][j].graphics = SuitCardGraphics(
                        ee_cards[i][j],
                        filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                    )
                    if tutorial:
                        ee_cards[i][j].graphics = SuitCardGraphics(
                            ee_cards[i][j],
                            filepath=Path("examples/pushmerge_zkp/images", f"{ee_cards[i][j].name}_tutorial.png"),
                        )
            
            ABB_CARDSQ[0].name = "heart"
            ABB_CARDSQ[1].name = "spade"
            ABB_CARDSQ[2].name = "spade"
            for card in ABB_CARDSQ:
                card.face_up = False
                card.graphics = SuitCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            AEB_CARDSQ[0].name = "heart"
            AEB_CARDSQ[1].name = "club"
            AEB_CARDSQ[2].name = "spade"
            for card in AEB_CARDSQ:
                card.face_up = False
                card.graphics = SuitCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            AED_CARDSQ[0].name = "heart"
            AED_CARDSQ[1].name = "club"
            AED_CARDSQ[2].name = "diamond"
            for card in AED_CARDSQ:
                card.face_up = False
                card.graphics = SuitCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            AEE_CARDSQ[0].name = "heart"
            AEE_CARDSQ[1].name = "club"
            AEE_CARDSQ[2].name = "club"
            for card in AEE_CARDSQ:
                card.face_up = False
                card.graphics = SuitCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            for (i, card) in enumerate(ENCODING_1_LENGTH_4):
                if i == 0:
                    card.name = "1"
                    card.number = 1
                else:
                    card.name = "0"
                    card.number = 0
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            for (i, card) in enumerate(ENCODING_2_LENGTH_4):
                if i == 1:
                    card.name = "1"
                    card.number = 1
                else:
                    card.name = "0"
                    card.number = 0
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            for (i, card) in enumerate(ENCODING_3_LENGTH_4):
                if i == 2:
                    card.name = "1"
                    card.number = 1
                else:
                    card.name = "0"
                    card.number = 0
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )
            for (i, card) in enumerate(ENCODING_4_LENGTH_4):
                if i == 3:
                    card.name = "1"
                    card.number = 1
                else:
                    card.name = "0"
                    card.number = 0
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/pushmerge_zkp/images", "card_back.png"),
                )
                if tutorial:
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/pushmerge_zkp/images", f"{card.name}_tutorial.png"),
                    )

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw(screen)
    pygame.display.flip()