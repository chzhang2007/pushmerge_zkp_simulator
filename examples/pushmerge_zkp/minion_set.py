from suit_card import SuitCard
from pygame_cards.set import CardsSet


MY_COMMUNITY_OF_THE_RING = CardsSet(
    [
        SuitCard("Bilbo", 5, 2, 2),
        SuitCard("Gandalf", 10, 6, 8),
        SuitCard("Sam", 7, 1, 2),
    ]
)

print(MY_COMMUNITY_OF_THE_RING)
