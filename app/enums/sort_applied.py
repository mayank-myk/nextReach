from enum import Enum


class SortApplied(Enum):
    RECOMMENDED = "Recommended"
    CONTENT_PRICE_LOW_TO_HIGH = "Content Price - Low To High"
    CONTENT_PRICE_HIGH_TO_LOW = "Content Price - High To Low"
    VIEWS_CHARGE_LOW_TO_HIGH = "Views Charge - Low To High"
    VIEWS_CHARGE_HIGH_TO_LOW = "Views Charge - High To Low"
