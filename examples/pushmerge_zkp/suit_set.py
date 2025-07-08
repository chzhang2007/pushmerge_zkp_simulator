from suit_card import SuitCard
from pygame_cards.set import CardsSet


ABB_CARDS = CardsSet(
    [
        SuitCard("heart", 0),
        SuitCard("spade", 1),
        SuitCard("spade", 1),
    ]
)

AEB_CARDS = CardsSet(
    [
        SuitCard("heart", 0),
        SuitCard("club", 2),
        SuitCard("spade", 1),
    ]
)

AEE_CARDS = CardsSet(
    [
        SuitCard("heart", 0),
        SuitCard("club", 2),
        SuitCard("club", 2),
    ]
)
