from enum import Enum


class ContentPrice(Enum):
    LE_5 = [0, 5000]
    BTN_5_10 = [5000, 10000]
    BTN_10_20 = [10000, 20000]
    GE_20 = [20000, 100000]
