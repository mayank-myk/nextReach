from enum import Enum


class AdminType(Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    BRANCH_MANAGER = "BRANCH_MANAGER"
    CALL_OPS = "CALL_OPS"
