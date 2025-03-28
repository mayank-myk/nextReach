from enum import Enum


class SortApplied(Enum):
    RECOMMENDED = "RECOMMENDED"
    CONTENT_PRICE_LOW_TO_HIGH = "CONTENT_PRICE_LOW_TO_HIGH"
    CONTENT_PRICE_HIGH_TO_LOW = "CONTENT_PRICE_HIGH_TO_LOW"
    VIEWS_CHARGE_LOW_TO_HIGH = "VIEWS_CHARGE_LOW_TO_HIGH"
    VIEWS_CHARGE_HIGH_TO_LOW = "VIEWS_CHARGE_HIGH_TO_LOW"
    BUDGET_HIGH_TO_LOW = "BUDGET_HIGH_TO_LOW"
    BUDGET_LOW_TO_HIGH = "BUDGET_LOW_TO_HIGH"
