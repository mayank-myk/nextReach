from enum import Enum


class InfluencerAge(Enum):
    LE_20 = "LE_20"
    BTN_20_25 = "BTN_20_25"
    BTN_25_30 = "BTN_25_30"
    BTN_30_35 = "BTN_30_35"
    BTN_35_40 = "BTN_35_40"
    BTN_40_50 = "BTN_40_50"
    GE_50 = "GE_50"


AGE_DICT = {
    InfluencerAge.LE_20: [0, 20],
    InfluencerAge.BTN_20_25: [20, 25],
    InfluencerAge.BTN_25_30: [25, 30],
    InfluencerAge.BTN_30_35: [30, 35],
    InfluencerAge.BTN_35_40: [35, 40],
    InfluencerAge.BTN_40_50: [40, 50],
    InfluencerAge.GE_50: [50, 100]
}
