from enum import Enum


class ReachPrice(Enum):
    LE_20 = "LE_20"
    BTN_20_30 = "BTN_20_30"
    BTN_30_40 = "BTN_30_40"
    BTN_40_50 = "BTN_40_50"
    BTN_50_60 = "BTN_50_60"
    GE_60 = "GE_60"


# Separate mapping for user-friendly display
REACH_PRICE_DICT = {
    ReachPrice.LE_20: [0, 20],
    ReachPrice.BTN_20_30: [20, 30],
    ReachPrice.BTN_30_40: [30, 40],
    ReachPrice.BTN_40_50: [40, 49],
    ReachPrice.BTN_50_60: [50, 60],
    ReachPrice.GE_60: [60, 1000]
}
