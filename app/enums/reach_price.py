from enum import Enum


class ReachPrice(Enum):
    LE_20 = "LE_20"
    BTN_20_29 = "BTN_20_29"
    BTN_30_39 = "BTN_30_39"
    BTN_40_49 = "BTN_40_49"
    BTN_50_59 = "BTN_50_59"
    GE_60 = "GE_60"


# Separate mapping for user-friendly display
REACH_PRICE_DICT = {
    ReachPrice.LE_20: [0, 20],
    ReachPrice.BTN_20_29: [20, 30],
    ReachPrice.BTN_30_39: [30, 40],
    ReachPrice.BTN_40_49: [40, 49],
    ReachPrice.BTN_50_59: [50, 60],
    ReachPrice.GE_60: [60, 1000]
}
