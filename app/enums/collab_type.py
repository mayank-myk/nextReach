from enum import Enum


class CollabType(Enum):
    CONTENT = "CONTENT"
    REACH = "REACH"
    CONTENT_AND_REACH = "CONTENT_AND_REACH"


COLLAB_TYPE_DICT = {
    CollabType.CONTENT: [CollabType.CONTENT],
    CollabType.REACH: [CollabType.REACH],
    CollabType.CONTENT_AND_REACH: [CollabType.CONTENT, CollabType.REACH, CollabType.CONTENT_AND_REACH]
}
