from enum import Enum


class Status(Enum):
    PROCESSING = "PROCESSING"
    IN_PROGRESS = "IN_PROGRESS"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
