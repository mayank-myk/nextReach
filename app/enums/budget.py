from enum import Enum


class Budget(Enum):
    LE_10 = "LE_10"
    BTN_10_25 = "BTN_10_25"
    BTN_25_50 = "BTN_25_50"
    BTN_50_75 = "BTN_50_75"
    BTN_75_100 = "BTN_75_100"
    GE_100 = "GE_100"


BUDGET_DICT = {
    Budget.LE_10: [0, 10],
    Budget.BTN_10_25: [10, 25],
    Budget.BTN_25_50: [25, 50],
    Budget.BTN_50_75: [50, 75],
    Budget.BTN_75_100: [75, 100],
    Budget.GE_100: [100, 1000]
}
