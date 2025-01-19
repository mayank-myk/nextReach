from enum import Enum


class ContentPrice(Enum):
    LE_5 = "LE_5"
    BTN_5_10 = "BTN_5_10"
    BTN_10_20 = "BTN_10_20"
    BTN_20_35 = "BTN_20_35"
    BTN_35_50 = "BTN_35_50"
    GE_50 = "GE_50"


CONTENT_PRICE_DICT = {
    ContentPrice.LE_5: [0, 5000],
    ContentPrice.BTN_5_10: [5000, 10000],
    ContentPrice.BTN_10_20: [10000, 20000],
    ContentPrice.BTN_20_35: [20000, 35000],
    ContentPrice.BTN_35_50: [35000, 50000],
    ContentPrice.GE_50: [50000, 1000000]
}
