from enum import Enum


class FollowerCount(Enum):
    LE_25 = "LE_25"
    BTN_25_100 = "BTN_25_100"
    BTN_100_250 = "BTN_100_250"
    BTN_250_500 = "BTN_250_500"
    BTN_500_1000 = "BTN_500_1000"
    GE_1000 = "GE_1000"


FOLLOWER_COUNT_DICT = {
    FollowerCount.LE_25: [0, 25000],
    FollowerCount.BTN_25_100: [25000, 100000],
    FollowerCount.BTN_100_250: [25000, 250000],
    FollowerCount.BTN_250_500: [250000, 500000],
    FollowerCount.BTN_500_1000: [500000, 1000000],
    FollowerCount.GE_1000: [1000000, 100000000]
}
