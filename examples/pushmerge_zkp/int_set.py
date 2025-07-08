from int_card import IntCard
from pygame_cards.set import CardsSet


INT_CARDS = CardsSet(
    [
        IntCard("1", True),
        IntCard("2", True),
        IntCard("3", True),
    ]
)

INT_CARDS_FACE_DOWN = CardsSet(
    [
        IntCard("1", False),
        IntCard("2", False),
        IntCard("3", False),
    ]
)
