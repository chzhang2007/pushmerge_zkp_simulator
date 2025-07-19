from int_card import IntCard
from pygame_cards.set import CardsSet


ID6 = CardsSet(
    [
        IntCard("1", True),
        IntCard("2", True),
        IntCard("3", True),
        IntCard("4", True),
        IntCard("5", True),
        IntCard("6", True),
    ]
)

ENCODING_MOVE_1 = CardsSet(
    [
        IntCard("0", False),
        IntCard("0", False),
        IntCard("0", False),
        IntCard("1", False),
        IntCard("2", False),
        IntCard("0", False),
    ]
)

ENCODING_MOVE_2 = CardsSet(
    [
        IntCard("0", False),
        IntCard("0", False),
        IntCard("0", False),
        IntCard("0", False),
        IntCard("1", False),
        IntCard("2", False),
    ]
)

ENCODING_MOVE_3 = CardsSet(
    [
        IntCard("0", False),
        IntCard("0", False),
        IntCard("2", False),
        IntCard("0", False),
        IntCard("0", False),
        IntCard("1", False),
    ]
)