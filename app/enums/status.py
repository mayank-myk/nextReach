from enum import Enum


class Status(Enum):
    PROCESSING = 1
    IN_PROGRESS = 2
    CANCELLED = 3
    COMPLETED = 4
