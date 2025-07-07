from minion_card import MinionCard
from pygame_cards.set import CardsSet


SUIT_CARDS = CardsSet(
    [
        MinionCard("Bilbo", 5, 2, 2),
        MinionCard("Gandalf", 10, 6, 8),
        MinionCard("Sam", 7, 1, 2),
    ]
)

print(SUIT_CARDS)
