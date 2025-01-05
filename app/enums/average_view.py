from enum import Enum


class AverageView(Enum):
    LE_100 = "LE_100"
    BTN_100_250 = "BTN_100_250"
    BTN_250_500 = "BTN_250_500"
    BTN_500_1000 = "BTN_500_1000"
    GE_1000 = "GE_1000"


VIEW_DICT = {
    AverageView.LE_100: [0, 100000],
    AverageView.BTN_100_250: [100000, 250000],
    AverageView.BTN_250_500: [250000, 500000],
    AverageView.BTN_500_1000: [500000, 1000000],
    AverageView.GE_1000: [1000000, 100000000]
}
