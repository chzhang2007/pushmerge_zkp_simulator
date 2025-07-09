from int_card import IntCard
from pygame_cards.set import CardsSet


ID3 = CardsSet(
    [
        IntCard("1", 1, True),
        IntCard("2", 2, True),
        IntCard("3", 3, True),
    ]
)

ID5 = CardsSet(
    [
        IntCard("1", 1, True),
        IntCard("2", 2, True),
        IntCard("3", 3, True),
        IntCard("4", 4, True),
        IntCard("5", 5, True),
    ]
)

DUMMY_ONE = CardsSet(
    [
        IntCard("1", 1, False),
        IntCard("1", 1, False),
        IntCard("1", 1, False),
        IntCard("1", 1, False),
    ]
)

DUMMY_TWO = CardsSet(
    [
        IntCard("2", 2, False),
        IntCard("2", 2, False),
        IntCard("2", 2, False),
        IntCard("2", 2, False),
    ]
)

DUMMY_THREE = CardsSet(
    [
        IntCard("3", 3, False),
        IntCard("3", 3, False),
        IntCard("3", 3, False),
        IntCard("3", 3, False),
    ]
)

DUMMY_FOUR = CardsSet(
    [
        IntCard("4", 4, False),
        IntCard("4", 4, False),
        IntCard("4", 4, False),
        IntCard("4", 4, False),
    ]
)

DUMMY_FIVE = CardsSet(
    [
        IntCard("5", 5, False),
        IntCard("5", 5, False),
        IntCard("5", 5, False),
        IntCard("5", 5, False),
    ]
)

ENCODING = CardsSet(
    [
        IntCard("0", 0, False),
        IntCard("0", 0, False),
        IntCard("0", 0, False),
        IntCard("1", 1, False),
        IntCard("0", 0, False),
    ]
)