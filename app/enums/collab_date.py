from enum import Enum


class CollabDate(Enum):
    DAYS_WITHIN_7 = "DAYS_WITHIN_7"
    DAYS_7_15 = "DAYS_7_15"
    DAYS_AFTER_15 = "DAYS_AFTER_15"


COLLAB_DATE_DICT = {
    CollabDate.DAYS_WITHIN_7: "Collab needed within 7 days",
    CollabDate.DAYS_7_15: "Collab needed within 7-15 days",
    CollabDate.DAYS_AFTER_15: "Collab needed after 15 days"
}
