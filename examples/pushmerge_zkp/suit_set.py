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
