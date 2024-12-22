from enum import Enum


class Status(Enum):
    PROCESSING = "processing"
    IN_PROGRESS = "in_progress"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
