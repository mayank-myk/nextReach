from enum import Enum


class AverageView(Enum):
    LE_100 = 1
    BTN_100_250 = 2
    BTN_250_500 = 3
    BTN_500_1000 = 4
    GE_1000 = 5
