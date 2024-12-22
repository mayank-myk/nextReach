from enum import Enum


class AverageView(Enum):
    LE_100 = [0, 100000]
    BTN_100_250 = [100000, 250000]
    BTN_250_500 = [250000, 500000]
    BTN_500_1000 = [500000, 1000000]
    GE_1000 = [1000000, 100000000]
