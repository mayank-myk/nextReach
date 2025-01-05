from enum import Enum


class EngagementRate(Enum):
    LE_1 = "LE_1"
    BTN_1_2 = "BTN_1_2"
    BTN_2_3 = "BTN_2_3"
    GE_4 = "GE_4"


ER_DICT = {
    EngagementRate.LE_1: [0, 1],
    EngagementRate.BTN_1_2: [1, 2],
    EngagementRate.BTN_2_3: [2, 3],
    EngagementRate.GE_4: [4, 100]
}
