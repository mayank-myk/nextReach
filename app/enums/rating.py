from enum import Enum


class Rating(Enum):
    GE_3 = "GE_3"
    GE_4 = "GE_4"


RATING_DICT = {
    Rating.GE_3: [3, 5],
    Rating.GE_4: [4, 5]
}
