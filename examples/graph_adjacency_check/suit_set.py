from suit_card import SuitCard
from pygame_cards.set import CardsSet


GRAPH_STATE = CardsSet(
    [
        SuitCard("diamond", True),
        SuitCard("diamond", True),
        SuitCard("spade", True),
        SuitCard("heart", True),
        SuitCard("club", True),
        SuitCard("spade", True),
    ]
)

AE = CardsSet(
    [
        SuitCard("heart", False),
        SuitCard("club", False),
    ]
)

AE_Q = CardsSet(
    [
        SuitCard("heart", False),
        SuitCard("club", False),
    ]
)

AG = CardsSet(
    [
        SuitCard("heart", False),
        SuitCard("spade", False),
    ]
)

AG_Q = CardsSet(
    [
        SuitCard("heart", False),
        SuitCard("spade", False),
    ]
)

ADJACENCY_COL_1 = CardsSet(
    [
        SuitCard("heart", True),
        SuitCard("diamond", True),
        SuitCard("club", True),
        SuitCard("diamond", True),
        SuitCard("club", True),
        SuitCard("club", True),
    ]
)

ADJACENCY_COL_1_COPY = CardsSet(
    [
        SuitCard("heart", False),
        SuitCard("diamond", False),
        SuitCard("club", False),
        SuitCard("diamond", False),
        SuitCard("club", False),
        SuitCard("club", False),
    ]
)

ADJACENCY_COL_2 = CardsSet(
    [
        SuitCard("diamond", True),
        SuitCard("heart", True),
        SuitCard("diamond", True),
        SuitCard("club", True),
        SuitCard("diamond", True),
        SuitCard("club", True),
    ]
)

ADJACENCY_COL_2_COPY = CardsSet(
    [
        SuitCard("diamond", False),
        SuitCard("heart", False),
        SuitCard("diamond", False),
        SuitCard("club", False),
        SuitCard("diamond", False),
        SuitCard("club", False),
    ]
)

ADJACENCY_COL_3 = CardsSet(
    [
        SuitCard("club", True),
        SuitCard("diamond", True),
        SuitCard("heart", True),
        SuitCard("club", True),
        SuitCard("club", True),
        SuitCard("diamond", True),
    ]
)

ADJACENCY_COL_3_COPY = CardsSet(
    [
        SuitCard("club", False),
        SuitCard("diamond", False),
        SuitCard("heart", False),
        SuitCard("club", False),
        SuitCard("club", False),
        SuitCard("diamond", False),
    ]
)

ADJACENCY_COL_4 = CardsSet(
    [
        SuitCard("diamond", True),
        SuitCard("club", True),
        SuitCard("club", True),
        SuitCard("heart", True),
        SuitCard("diamond", True),
        SuitCard("club", True),
    ]
)

ADJACENCY_COL_4_COPY = CardsSet(
    [
        SuitCard("diamond", False),
        SuitCard("club", False),
        SuitCard("club", False),
        SuitCard("heart", False),
        SuitCard("diamond", False),
        SuitCard("club", False),
    ]
)

ADJACENCY_COL_5 = CardsSet(
    [
        SuitCard("club", True),
        SuitCard("diamond", True),
        SuitCard("club", True),
        SuitCard("diamond", True),
        SuitCard("heart", True),
        SuitCard("diamond", True),
    ]
)

ADJACENCY_COL_5_COPY = CardsSet(
    [
        SuitCard("club", False),
        SuitCard("diamond", False),
        SuitCard("club", False),
        SuitCard("diamond", False),
        SuitCard("heart", False),
        SuitCard("diamond", False),
    ]
)

ADJACENCY_COL_6 = CardsSet(
    [
        SuitCard("club", True),
        SuitCard("club", True),
        SuitCard("diamond", True),
        SuitCard("club", True),
        SuitCard("diamond", True),
        SuitCard("heart", True),
    ]
)

ADJACENCY_COL_6_COPY = CardsSet(
    [
        SuitCard("club", False),
        SuitCard("club", False),
        SuitCard("diamond", False),
        SuitCard("club", False),
        SuitCard("diamond", False),
        SuitCard("heart", False),
    ]
)