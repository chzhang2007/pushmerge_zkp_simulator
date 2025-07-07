from suit_card import SuitCard
from pygame_cards.set import CardsSet


SUIT_CARDS = CardsSet(
    [
        SuitCard("heart", 5, 2, 2),
        SuitCard("spade", 3, 4, 5),
        SuitCard("club", 10, 6, 8),
        SuitCard("diamond", 7, 1, 2),
    ]
)

print(SUIT_CARDS)
