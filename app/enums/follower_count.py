from enum import Enum


class FollowerCount(Enum):
    LE_25 = 1
    BTN_25_100 = 2
    BTN_100_250 = 3
    BTN_250_500 = 4
    BTN_500_1000 = 5
    GE_1000 = 6
