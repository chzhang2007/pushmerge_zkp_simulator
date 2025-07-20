import random
import sys
import copy
import pygame
from pathlib import Path
from suit_card import SuitCard
from suit_card_graphics import SuitCardGraphics
from int_card_graphics import IntCardGraphics
from letter_card_graphics import LetterCardGraphics
from pygame_cards.abstract import AbstractCard
from pygame_cards.back import CardBackGraphics
from pygame_cards.hands import AlignedHand, AlignedHandVertical
from pygame_cards.manager import CardSetRights, CardsManager

from suit_set import MANIFOLD_STATE, AE, AG
from int_set import ID2, ID6, ENCODING_MOVE_1, ENCODING_MOVE_2, ENCODING_MOVE_3
from letter_set import ADJACENCY_COL_1, ADJACENCY_COL_2, ADJACENCY_COL_3, ADJACENCY_COL_4, ADJACENCY_COL_5, ADJACENCY_COL_6, ADJACENCY_COL_1_COPY, ADJACENCY_COL_2_COPY, ADJACENCY_COL_3_COPY, ADJACENCY_COL_4_COPY, ADJACENCY_COL_5_COPY, ADJACENCY_COL_6_COPY
from pygame_cards.set import CardsSet

pygame.init()


screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
size = width, height = screen.get_size()


manager = CardsManager()

id_cards_m = ID6


# TO CHANGE INPUT: MODIFY HERE (INPUTS RESTRICTED TO A 6-VERTEX MANIFOLD)
grid_state_m = MANIFOLD_STATE # initial grid state
number_of_moves = 3
# to modify encoding_rows_m, go into int_set.py and modify the sets ENCODING_MOVE_1, ENCODING_MOVE_2, etc.
encoding_rows_m = [ENCODING_MOVE_1.copy(), ENCODING_MOVE_2.copy(), ENCODING_MOVE_3.copy()]
# modify encoding_1_m and encoding_1_n (1-indexed) to match encoding_rows_m and encoding_rows_n
encoding_1 = [4, 5, 6]
encoding_2 = [5, 6, 3]
# to modify the adjacency matrix, go into letter_set.py and modify the sets
adjacency_matrix = [ADJACENCY_COL_1.copy(), ADJACENCY_COL_2.copy(), ADJACENCY_COL_3.copy(), ADJACENCY_COL_4.copy(), ADJACENCY_COL_5.copy(), ADJACENCY_COL_6.copy()]
adjacency_matrix_copy = [ADJACENCY_COL_1_COPY.copy(), ADJACENCY_COL_2_COPY.copy(), ADJACENCY_COL_3_COPY.copy(), ADJACENCY_COL_4_COPY.copy(), ADJACENCY_COL_5_COPY.copy(), ADJACENCY_COL_6_COPY.copy()]
# modify the target position (1-indexed) to match the manifold reachability instance
target_pos = 3
# if tutorial, face-down cards will be visible
tutorial = False

card_size = (width / 28, height / 12 - 10)
card_set_size_wide = (width - 10, height / 12)
card_set_size_long = (width / 28, height / 2)

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
adjacency_matrix_graphics = [AlignedHandVertical(
    adjacency_matrix[i],
    card_set_size_long,
    card_size=card_size,
    graphics_type=LetterCardGraphics,
) for i in range(len(adjacency_matrix))]
for (i, adj_graphics) in enumerate(adjacency_matrix_graphics):
    manager.add_set(
        adj_graphics,
        (i * (card_set_size_long[0] + 7), 2 * id_cards_m_graphics.size[1] + 10),
    )

card_back = AbstractCard("")
card_back.graphics_type = CardBackGraphics

pygame.display.flip()

clock = pygame.time.Clock()

stage = -1

p_shuffled = 0
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
                    filepath=Path("examples/manifold_adjacency_check/images", "card_back.png"),
                )
            for card in grid_state_m_graphics.cardset:
                card.face_up = False
                card.graphics = SuitCardGraphics(
                    card,
                    filepath=Path("examples/manifold_adjacency_check/images", "card_back.png"),
                )
            for adj_graphics in adjacency_matrix_graphics:
                for card in adj_graphics.cardset:
                    card.face_up = False
                    card.graphics = LetterCardGraphics(
                        card,
                        filepath=Path("examples/manifold_adjacency_check/images", "card_back.png"),
                    )
            stage = 0
            id_cards_m_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            for adj_graphics in adjacency_matrix_graphics:
                adj_graphics.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and current_move >= number_of_moves:
            if current_move == number_of_moves:
                # turn the card at the target position face-up to ensure it is the agent
                grid_state_m_graphics.cardset[target_pos - 1].face_up = True
                grid_state_m_graphics.cardset[target_pos - 1].graphics = SuitCardGraphics(
                    grid_state_m_graphics.cardset[target_pos - 1],
                    filepath=Path("examples/manifold_adjacency_check/images", f"{grid_state_m_graphics.cardset[target_pos - 1].name}.png"),
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
                (0, 8 * grid_state_m_graphics.size[1]),
            )
            if tutorial:
                for (i, card) in enumerate(enc_cards_m_graphics.cardset):
                    card.graphics = IntCardGraphics(
                        card,
                        filepath=Path("examples/manifold_adjacency_check/images", f"{card.name}_tutorial.png"),
                    )
            
            # generate random pile shifting shuffle
            index_list = [(i + 1) for i in range(len(id_cards_m))]
            random.shuffle(index_list)
            
            # flip the id cards face down and shuffle them
            for (i, card) in enumerate(id_cards_m):
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
                if index_list[i] == encoding_1[current_move]:
                    card.name = "1"
                    card.number = 1
                elif index_list[i] == encoding_2[current_move]:
                    card.name = "2"
                    card.number = 2
                else:
                    card.name = "0"
                    card.number = 0
                    
            # shuffle the adjacency matrix
            for (i, column) in enumerate(adjacency_matrix_graphics):
                for j in range(6):
                    column.append_card(adjacency_matrix_graphics[index_list[i] - 1].cardset[j])
            for column in adjacency_matrix_graphics:
                for j in range(6):
                    column.remove_card(column.cardset[0])

            stage = 1
            id_cards_m_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            enc_cards_m_graphics.clear_cache()
            for adj_graphics in adjacency_matrix_graphics:
                adj_graphics.clear_cache()

        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 1:
            # turn the encoding row face up
            for card in enc_cards_m_graphics.cardset:
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/manifold_adjacency_check/images", f"{card.name}.png"),
                )

            stage = 2
            id_cards_m_graphics.clear_cache()
            grid_state_m_graphics.clear_cache()
            enc_cards_m_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 2:
            grid_state_n = AE.copy()
            adjacency_matrix_n = [adjacency_matrix_copy[encoding_1[current_move] - 1], 
                                  adjacency_matrix_copy[encoding_2[current_move] - 1]]
            for (i, card) in enumerate(enc_cards_m_graphics.cardset):
                if card.name == "1":
                    grid_state_m_graphics.cardset[i].name = "blank"
                    grid_state_m_graphics.cardset[i].graphics = SuitCardGraphics(
                        grid_state_m_graphics.cardset[i],
                        filepath=Path("examples/manifold_adjacency_check/images", "blank.png"),
                    )
                    for adj_card in adjacency_matrix_graphics[i].cardset:
                        adj_card.graphics = LetterCardGraphics(
                            adj_card,
                            filepath=Path("examples/manifold_adjacency_check/images", "blank.png"),
                        )
                elif card.name == "2":
                    if grid_state_m_graphics.cardset[i].name == "spade":
                        grid_state_n = AG.copy()
                    grid_state_m_graphics.cardset[i].name = "blank"
                    grid_state_m_graphics.cardset[i].graphics = SuitCardGraphics(
                        grid_state_m_graphics.cardset[i],
                        filepath=Path("examples/manifold_adjacency_check/images", "blank.png"),
                    )
                    for adj_card in adjacency_matrix_graphics[i].cardset:
                        adj_card.graphics = LetterCardGraphics(
                            adj_card,
                            filepath=Path("examples/manifold_adjacency_check/images", "blank.png"),
                        )

            grid_state_n_graphics = AlignedHand(
                grid_state_n,
                card_set_size_wide,
                card_size=card_size,
                graphics_type=SuitCardGraphics,
            )
            manager.add_set(
                grid_state_n_graphics,
                (9 * (card_set_size_long[0] + 7), 0),
            )

            adjacency_matrix_n_graphics = [AlignedHandVertical(
                adjacency_matrix_n[i],
                card_set_size_long,
                card_size=card_size,
                graphics_type=LetterCardGraphics,
            ) for i in range(len(adjacency_matrix_n))]
            
            for i in range(2):
                manager.add_set(
                    adjacency_matrix_n_graphics[i],
                    ((9 + i) * (card_set_size_long[0] + 7), card_set_size_wide[1]),
                )
            
            stage = 3
            grid_state_m_graphics.clear_cache()
            grid_state_n_graphics.clear_cache()
            for adj_graphics in adjacency_matrix_graphics:
                adj_graphics.clear_cache()
            for adj_graphics in adjacency_matrix_n_graphics:
                adj_graphics.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 3:
            # form the id row of matrix Q
            id_cards_q = ID2.copy()
            id_cards_q_graphics = AlignedHand(
                id_cards_q,
                card_set_size_wide,
                card_size=card_size,
                graphics_type=IntCardGraphics,
            )
            manager.add_set(
                id_cards_q_graphics,
                (9 * (card_set_size_long[0] + 7), 8 * grid_state_m_graphics.size[1]),
            )
            
            stage = 4

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw(screen)
    pygame.display.flip()