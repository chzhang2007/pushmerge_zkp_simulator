from suit_card import SuitCard
from pygame_cards.set import CardsSet


SUIT_CARDS = CardsSet(
    [
        SuitCard("heart", 0),
        SuitCard("spade", 1),
        SuitCard("club", 2),
        SuitCard("diamond", 3),
    ]
)

print(SUIT_CARDS)
