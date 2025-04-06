from enum import Enum


class Budget(Enum):
    LE_10 = "LE_10"
    BTN_10_25 = "BTN_10_25"
    BTN_25_50 = "BTN_25_50"
    BTN_50_75 = "BTN_50_75"
    BTN_75_100 = "BTN_75_100"
    GE_100 = "GE_100"


BUDGET_DICT = {
    Budget.LE_10: [0, 13000],
    Budget.BTN_10_25: [8000, 30000],
    Budget.BTN_25_50: [20000, 60000],
    Budget.BTN_50_75: [40000, 90000],
    Budget.BTN_75_100: [60000, 130000],
    Budget.GE_100: [80000, 10000000]
}
