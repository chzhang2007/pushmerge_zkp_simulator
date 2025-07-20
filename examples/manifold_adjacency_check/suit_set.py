from suit_card import SuitCard
from pygame_cards.set import CardsSet


MANIFOLD_STATE = CardsSet(
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

AG = CardsSet(
    [
        SuitCard("heart", False),
        SuitCard("spade", False),
    ]
)
