from suit_card import SuitCard
from pygame_cards.set import CardsSet


ABB_CARDS = CardsSet(
    [
        SuitCard("heart", False),
        SuitCard("spade", False),
        SuitCard("spade", False),
    ]
)

AEB_CARDS = CardsSet(
    [
        SuitCard("heart", False),
        SuitCard("club", False),
        SuitCard("spade", False),
    ]
)

AEE_CARDS = CardsSet(
    [
        SuitCard("heart", False),
        SuitCard("club", False),
        SuitCard("club", False),
    ]
)

AED_CARDS = CardsSet(
    [
        SuitCard("heart", False),
        SuitCard("club", False),
        SuitCard("diamond", False),
    ]
)

DUMMY_LENGTH_4 = CardsSet(
    [
        SuitCard("diamond", False),
        SuitCard("diamond", False),
        SuitCard("diamond", False),
        SuitCard("diamond", False),
    ]
)

GRID_STATE = CardsSet(
    [
        SuitCard("diamond", True),
        SuitCard("diamond", True),
        SuitCard("diamond", True),
        SuitCard("diamond", True),
        SuitCard("diamond", True),
        SuitCard("diamond", True),
        SuitCard("spade", True),
        SuitCard("club", True),
        SuitCard("club", True),
        SuitCard("diamond", True),
        SuitCard("diamond", True),
        SuitCard("heart", True),
        SuitCard("spade", True),
        SuitCard("spade", True),
        SuitCard("diamond", True),
        SuitCard("diamond", True),
        SuitCard("diamond", True),
        SuitCard("diamond", True),
        SuitCard("diamond", True),
        SuitCard("diamond", True),
    ]
)