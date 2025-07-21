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

from suit_set import GRAPH_STATE, AE, AE_Q, AG, AG_Q, ADJACENCY_COL_1, ADJACENCY_COL_2, ADJACENCY_COL_3, ADJACENCY_COL_4, ADJACENCY_COL_5, ADJACENCY_COL_6, ADJACENCY_COL_1_COPY, ADJACENCY_COL_2_COPY, ADJACENCY_COL_3_COPY, ADJACENCY_COL_4_COPY, ADJACENCY_COL_5_COPY, ADJACENCY_COL_6_COPY
from int_set import ID2, ID6, ID6_COPY, ENCODING_MOVE_1, ENCODING_MOVE_2, ENCODING_MOVE_3, ENCODING_MOVE_1_COPY, ENCODING_MOVE_2_COPY, ENCODING_MOVE_3_COPY
from pygame_cards.set import CardsSet

pygame.init()


screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
size = width, height = screen.get_size()


manager = CardsManager()

id_cards_m = ID6.copy()

# TO CHANGE INPUT: MODIFY HERE (INPUTS RESTRICTED TO A 6-VERTEX graph)
grid_state_m = GRAPH_STATE # initial grid state
number_of_moves = 3
# to modify encoding_rows_m, go into int_set.py and modify the sets ENCODING_MOVE_1, ENCODING_MOVE_2, etc.
encoding_rows_m = [ENCODING_MOVE_1.copy(), ENCODING_MOVE_2.copy(), ENCODING_MOVE_3.copy()]
encoding_rows_n = [ENCODING_MOVE_1_COPY.copy(), ENCODING_MOVE_2_COPY.copy(), ENCODING_MOVE_3_COPY.copy()]
# modify encoding_1_m and encoding_1_n (1-indexed) to match encoding_rows_m and encoding_rows_n
encoding_1 = [4, 5, 6]
encoding_2 = [5, 6, 3]
# to modify the adjacency matrix, go into letter_set.py and modify the sets
adjacency_matrix = [ADJACENCY_COL_1.copy(), ADJACENCY_COL_2.copy(), ADJACENCY_COL_3.copy(), ADJACENCY_COL_4.copy(), ADJACENCY_COL_5.copy(), ADJACENCY_COL_6.copy()]
adjacency_matrix_copy = [ADJACENCY_COL_1_COPY.copy(), ADJACENCY_COL_2_COPY.copy(), ADJACENCY_COL_3_COPY.copy(), ADJACENCY_COL_4_COPY.copy(), ADJACENCY_COL_5_COPY.copy(), ADJACENCY_COL_6_COPY.copy()]
# modify the target position (1-indexed) to match the graph reachability instance
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
    graphics_type=SuitCardGraphics,
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
                    filepath=Path("examples/graph_adjacency_check/images", "card_back.png"),
                )
            for card in grid_state_m_graphics.cardset:
                card.face_up = False
                card.graphics = SuitCardGraphics(
                    card,
                    filepath=Path("examples/graph_adjacency_check/images", "card_back.png"),
                )
            for adj_graphics in adjacency_matrix_graphics:
                for card in adj_graphics.cardset:
                    card.face_up = False
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/graph_adjacency_check/images", "card_back.png"),
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
                    filepath=Path("examples/graph_adjacency_check/images", f"{grid_state_m_graphics.cardset[target_pos - 1].name}.png"),
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
                        filepath=Path("examples/graph_adjacency_check/images", f"{card.name}_tutorial.png"),
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
                    filepath=Path("examples/graph_adjacency_check/images", f"{card.name}.png"),
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
                        filepath=Path("examples/graph_adjacency_check/images", "blank.png"),
                    )
                    for adj_card in adjacency_matrix_graphics[i].cardset:
                        adj_card.graphics = SuitCardGraphics(
                            adj_card,
                            filepath=Path("examples/graph_adjacency_check/images", "blank.png"),
                        )
                elif card.name == "2":
                    if grid_state_m_graphics.cardset[i].name == "spade":
                        grid_state_n = AG.copy()
                    grid_state_m_graphics.cardset[i].name = "blank"
                    grid_state_m_graphics.cardset[i].graphics = SuitCardGraphics(
                        grid_state_m_graphics.cardset[i],
                        filepath=Path("examples/graph_adjacency_check/images", "blank.png"),
                    )
                    for adj_card in adjacency_matrix_graphics[i].cardset:
                        adj_card.graphics = SuitCardGraphics(
                            adj_card,
                            filepath=Path("examples/graph_adjacency_check/images", "blank.png"),
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
                graphics_type=SuitCardGraphics,
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
            # form the id column of matrix Q
            id_cards_q = ID2.copy()
            id_cards_q_graphics = AlignedHandVertical(
                id_cards_q,
                card_set_size_long,
                card_size=card_size,
                graphics_type=IntCardGraphics,
            )
            manager.add_set(
                id_cards_q_graphics,
                (9 * (card_set_size_long[0] + 7), 8 * grid_state_m_graphics.size[1]),
            )
            
            stage = 4
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 4:
            # form the grid state rows of matrix Q
            grid_state_q = [AE_Q.copy(), AG_Q.copy()]
            if grid_state_n_graphics.cardset[1].name == "spade":
                grid_state_q = [AG_Q.copy(), AE_Q.copy()]
                
            grid_state_q_graphics = [AlignedHand(
                grid_state_q[i],
                card_set_size_wide,
                card_size=card_size,
                graphics_type=SuitCardGraphics,
            ) for i in range(len(grid_state_q))]
            
            for i in range(2):
                manager.add_set(
                    grid_state_q_graphics[i],
                    (10 * (card_set_size_long[0] + 7), (i + 8) * card_set_size_wide[1] - 6),
                )
                
            # remove the grid state row from matrix N
            for card in grid_state_n_graphics.cardset:
                card.graphics = SuitCardGraphics(
                    card,
                    filepath=Path("examples/graph_adjacency_check/images", "blank.png"),
                )
                
            stage = 5
            grid_state_n_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 5:
            # turn the id column of matrix Q face down
            for card in id_cards_q_graphics.cardset:
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/graph_adjacency_check/images", "card_back.png"),
                )
                
            # shuffle the rows of matrix Q
            shuffle = random.choice([0, 1])
            if shuffle == 1:
                id_cards_q_graphics.cardset[0].name = "2"
                id_cards_q_graphics.cardset[1].name = "1"
                if grid_state_q_graphics[0].cardset[1].name == "club":
                    grid_state_q_graphics[0].cardset[1].name = "spade"
                    grid_state_q_graphics[1].cardset[1].name = "club"
                else:
                    grid_state_q_graphics[0].cardset[1].name = "club"
                    grid_state_q_graphics[1].cardset[1].name = "spade"
            
            stage = 6
            id_cards_q_graphics.clear_cache()
            for row in grid_state_q_graphics:
                row.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 6:
            # turn the grid state rows of matrix Q face up
            for row in grid_state_q_graphics:
                for card in row.cardset:
                    card.face_up = True
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/graph_adjacency_check/images", f"{card.name}.png"),
                    )
                    
            stage = 7
            for row in grid_state_q_graphics:
                row.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 7:
            # simulate the replacement rule for each row in matrix Q
            for i in range(2):
                if grid_state_q_graphics[i].cardset[1].name == "spade":
                    grid_state_q_graphics[i].cardset[0].name = "diamond"
                    grid_state_q_graphics[i].cardset[0].graphics = SuitCardGraphics(
                        grid_state_q_graphics[i].cardset[0],
                        filepath=Path("examples/graph_adjacency_check/images", "diamond.png"),
                    )
                    grid_state_q_graphics[i].cardset[1].name = "heart"
                    grid_state_q_graphics[i].cardset[1].graphics = SuitCardGraphics(
                        grid_state_q_graphics[i].cardset[1],
                        filepath=Path("examples/graph_adjacency_check/images", "heart.png"),
                    )
                else:
                    grid_state_q_graphics[i].cardset[0].name = "club"
                    grid_state_q_graphics[i].cardset[0].graphics = SuitCardGraphics(
                        grid_state_q_graphics[i].cardset[0],
                        filepath=Path("examples/graph_adjacency_check/images", "club.png"),
                    )
                    grid_state_q_graphics[i].cardset[1].name = "heart"
                    grid_state_q_graphics[i].cardset[1].graphics = SuitCardGraphics(
                        grid_state_q_graphics[i].cardset[1],
                        filepath=Path("examples/graph_adjacency_check/images", "heart.png"),
                    )
                    
            stage = 8
            for row in grid_state_q_graphics:
                row.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 8:
            # turn the grid state rows of matrix Q face down
            for row in grid_state_q_graphics:
                for card in row.cardset:
                    card.face_up = False
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/graph_adjacency_check/images", "card_back.png"),
                    )
                    
            # shuffle the rows of matrix Q
            shuffle = random.choice([0, 1])
            if shuffle == 1:
                id_cards_q_graphics.cardset[0].name = str(3 - int(id_cards_q_graphics.cardset[0].name))
                id_cards_q_graphics.cardset[1].name = str(3 - int(id_cards_q_graphics.cardset[0].name))
                if grid_state_q_graphics[0].cardset[0].name == "club":
                    grid_state_q_graphics[0].cardset[0].name = "diamond"
                    grid_state_q_graphics[1].cardset[0].name = "club"
                else:
                    grid_state_q_graphics[0].cardset[0].name = "club"
                    grid_state_q_graphics[1].cardset[0].name = "diamond"

            stage = 9
            id_cards_q_graphics.clear_cache()
            for row in grid_state_q_graphics:
                row.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 9:
            # turn the id column of matrix Q face up
            for card in id_cards_q_graphics.cardset:
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/graph_adjacency_check/images", f"{card.name}.png"),
                )
                
            stage = 10
            id_cards_q_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 10:
            # return the rows of matrix Q to their original ordering
            if id_cards_q_graphics.cardset[0].name == "2":
                id_cards_q_graphics.cardset[0].name = "1"
                id_cards_q_graphics.cardset[0].graphics = IntCardGraphics(
                    id_cards_q_graphics.cardset[0],
                    filepath=Path("examples/graph_adjacency_check/images", "1.png"),
                )
                id_cards_q_graphics.cardset[1].name = "2"
                id_cards_q_graphics.cardset[1].graphics = IntCardGraphics(
                    id_cards_q_graphics.cardset[1],
                    filepath=Path("examples/graph_adjacency_check/images", "2.png"),
                )
                if grid_state_q_graphics[0].cardset[0].name == "club":
                    grid_state_q_graphics[0].cardset[0].name = "diamond"
                    grid_state_q_graphics[1].cardset[0].name = "club"
                else:
                    grid_state_q_graphics[0].cardset[0].name = "club"
                    grid_state_q_graphics[1].cardset[0].name = "diamond"
            
            stage = 11
            id_cards_q_graphics.clear_cache()
            for row in grid_state_q_graphics:
                row.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 11:
            # return the first row of matrix Q to matrix N
            for (i, card) in enumerate(grid_state_n_graphics.cardset):
                card.name = grid_state_q_graphics[0].cardset[i].name
                card.face_up = False
                card.graphics = SuitCardGraphics(
                    card,
                    filepath=Path("examples/graph_adjacency_check/images", "card_back.png"),
                )
                
            # discard the rest of matrix Q
            for i in range(2):
                grid_state_q_graphics[i].remove_all_cards()
            id_cards_q_graphics.remove_all_cards()
            
            stage = 12
            grid_state_n_graphics.clear_cache()
            id_cards_q_graphics.clear_cache()
            for row in grid_state_q_graphics:
                row.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 12:
            # place the identity column to the left of N
            id_cards_n = ID6_COPY.copy()
            id_cards_n_graphics = AlignedHandVertical(
                id_cards_n,
                card_set_size_long,
                card_size=card_size,
            )
            manager.add_set(
                id_cards_n_graphics,
                (8 * (card_set_size_long[0] + 7), card_set_size_wide[1]),
            )
            
            stage = 13
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 13:
            # turn the id column face down
            for card in id_cards_n_graphics.cardset:
                card.face_up = False
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/graph_adjacency_check/images", "card_back.png"),
                )
            
            stage = 14
            id_cards_n_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 14:
            enc_cards_n = encoding_rows_n[current_move].copy()
            enc_cards_n_graphics = AlignedHandVertical(
                enc_cards_n,
                card_set_size_long,
                card_size=card_size,
                graphics_type=IntCardGraphics,
            )
            manager.add_set(
                enc_cards_n_graphics,
                (11 * (card_set_size_long[0] + 7), card_set_size_wide[1]),
            )
            
            # shuffle the rows of matrix N
            index_list = [(i + 1) for i in range(len(id_cards_n_graphics.cardset))]
            random.shuffle(index_list)

            # shuffle the id column
            id_card_numbers = [int(card.name) for card in id_cards_n_graphics.cardset]
            for (i, card) in enumerate(id_cards_n_graphics.cardset):
                card.name = str(id_card_numbers[index_list[i] - 1])
                card.number = id_card_numbers[index_list[i] - 1]
                
            # shuffle the rows of the adjacency matrix
            for i in range(len(id_cards_n_graphics.cardset)):
                adjacency_matrix_n_graphics[0].append_card(adjacency_matrix_n_graphics[0].cardset[index_list[i] - 1])
                adjacency_matrix_n_graphics[1].append_card(adjacency_matrix_n_graphics[1].cardset[index_list[i] - 1])

            for i in range(len(id_cards_n_graphics.cardset)):
                adjacency_matrix_n_graphics[0].remove_card(adjacency_matrix_n_graphics[0].cardset[0])
                adjacency_matrix_n_graphics[1].remove_card(adjacency_matrix_n_graphics[1].cardset[0])
                    
            # shuffle the encoding column
            for (i, card) in enumerate(enc_cards_n_graphics.cardset):
                if index_list[i] == encoding_1[current_move]:
                    card.name = "1"
                    card.number = 1
                elif index_list[i] == encoding_2[current_move]:
                    card.name = "2"
                    card.number = 2
                else:
                    card.name = "0"
                    card.number = 0
            
            stage = 15
            id_cards_n_graphics.clear_cache()
            enc_cards_n_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 15:
            # turn the encoding column face up
            for card in enc_cards_n_graphics.cardset:
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/graph_adjacency_check/images", f"{card.name}.png"),
                )
                
            stage = 16
            enc_cards_n_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 16:
            # turn the heart cards face up
            for (i, card) in enumerate(adjacency_matrix_n_graphics[0].cardset):
                if enc_cards_n_graphics.cardset[i].name == "1":
                    card.face_up = True
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/graph_adjacency_check/images", f"{card.name}.png"),
                    )
            for (i, card) in enumerate(adjacency_matrix_n_graphics[1].cardset):
                if enc_cards_n_graphics.cardset[i].name == "2":
                    card.face_up = True
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/graph_adjacency_check/images", f"{card.name}.png"),
                    )
                    
            stage = 17
            for adj_graphics in adjacency_matrix_n_graphics:
                adj_graphics.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 17:
            # turn the heart cards face down
            for (i, card) in enumerate(adjacency_matrix_n_graphics[0].cardset):
                if enc_cards_n_graphics.cardset[i].name == "1":
                    card.face_up = False
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/graph_adjacency_check/images", "card_back.png"),
                    )
            for (i, card) in enumerate(adjacency_matrix_n_graphics[1].cardset):
                if enc_cards_n_graphics.cardset[i].name == "2":
                    card.face_up = False
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/graph_adjacency_check/images", "card_back.png"),
                    )
            
            stage = 18
            for adj_graphics in adjacency_matrix_n_graphics:
                adj_graphics.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 18:
            # confirm that the two positions are adjacent
            for (i, card) in enumerate(adjacency_matrix_n_graphics[1].cardset):
                if enc_cards_n_graphics.cardset[i].name == "1":
                    card.face_up = True
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/graph_adjacency_check/images", f"{card.name}.png"),
                    )
                    
            stage = 19
            for adj_graphics in adjacency_matrix_n_graphics:
                adj_graphics.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 19:
            # turn the diamond card face down
            for (i, card) in enumerate(adjacency_matrix_n_graphics[1].cardset):
                if enc_cards_n_graphics.cardset[i].name == "1":
                    card.face_up = False
                    card.graphics = SuitCardGraphics(
                        card,
                        filepath=Path("examples/graph_adjacency_check/images", "card_back.png"),
                    )
                    
            stage = 20
            for adj_graphics in adjacency_matrix_n_graphics:
                adj_graphics.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 20:
            # discard the encoding column
            enc_cards_n_graphics.remove_all_cards()
            
            # shuffle the rows of matrix N
            index_list = [(i + 1) for i in range(len(id_cards_n_graphics.cardset))]
            random.shuffle(index_list)
            
            # shuffle the id column
            id_card_numbers = [int(card.name) for card in id_cards_n_graphics.cardset]
            for (i, card) in enumerate(id_cards_n_graphics.cardset):
                card.name = str(id_card_numbers[index_list[i] - 1])
                card.number = id_card_numbers[index_list[i] - 1]
                
            # shuffle the rows of the adjacency matrix
            for i in range(len(id_cards_n_graphics.cardset)):
                adjacency_matrix_n_graphics[0].append_card(adjacency_matrix_n_graphics[0].cardset[index_list[i] - 1])
                adjacency_matrix_n_graphics[1].append_card(adjacency_matrix_n_graphics[1].cardset[index_list[i] - 1])

            for i in range(len(id_cards_n_graphics.cardset)):
                adjacency_matrix_n_graphics[0].remove_card(adjacency_matrix_n_graphics[0].cardset[0])
                adjacency_matrix_n_graphics[1].remove_card(adjacency_matrix_n_graphics[1].cardset[0])
            
            stage = 21
            id_cards_n_graphics.clear_cache()
            for adj_graphics in adjacency_matrix_n_graphics:
                adj_graphics.clear_cache()
                
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 21:
            # turn the id column face up
            for card in id_cards_n_graphics.cardset:
                card.face_up = True
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/graph_adjacency_check/images", f"{card.name}.png"),
                )
                
            stage = 22
            id_cards_n_graphics.clear_cache()
            
        elif event.type == pygame.MOUSEBUTTONDOWN and stage == 22:
            # return the rows of the adjacency matrix to their original positions
            adjacency_matrix_n_temp = [[0 for _ in range(6)] for _ in range(2)]
            for (i, card) in enumerate(adjacency_matrix_n_graphics[0].cardset):
                adjacency_matrix_n_temp[0][id_cards_n[i].number - 1] = card
            for (i, card) in enumerate(adjacency_matrix_n_graphics[1].cardset):
                adjacency_matrix_n_temp[1][id_cards_n[i].number - 1] = card
            adjacency_matrix_n = adjacency_matrix_n_temp
            adjacency_matrix_n_graphics[0].cardset = adjacency_matrix_n_temp[0]
            adjacency_matrix_n_graphics[1].cardset = adjacency_matrix_n_temp[1]

            # return the id column to its original ordering
            for (i, card) in enumerate(id_cards_n_graphics.cardset):
                card.name = str(i + 1)
                card.graphics = IntCardGraphics(
                    card,
                    filepath=Path("examples/graph_adjacency_check/images", f"{card.name}.png"),
                )
            
            stage = 23
            id_cards_n_graphics.clear_cache()
            for adj_graphics in adjacency_matrix_n_graphics:
                adj_graphics.clear_cache()

        manager.process_events(event)

    manager.update(time_delta)
    manager.draw(screen)
    pygame.display.flip()