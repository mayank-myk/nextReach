from enum import Enum


class ReachPrice(Enum):
    LE_20 = [0, 20]
    BTN_20_29 = [20, 30]
    BTN_30_39 = [30, 40]
    BTN_40_49 = [40, 49]
    BTN_50_59 = [50, 60]
    GE_60 = [60, 1000]
