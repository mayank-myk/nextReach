from enum import Enum


class ContentPrice(Enum):
    LE_5 = "LE_5"
    BTN_5_10 = "BTN_5_10"
    BTN_10_20 = "BTN_10_20"
    GE_20 = "GE_20"


CONTENT_PRICE_DICT = {
    ContentPrice.LE_5: [0, 5000],
    ContentPrice.BTN_5_10: [5000, 10000],
    ContentPrice.BTN_10_20: [10000, 20000],
    ContentPrice.GE_20: [20000, 100000]
}
