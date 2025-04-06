from enum import Enum


class ContentType(Enum):
    PROMOTIONAL = "PROMOTIONAL"
    NON_PROMOTIONAL = "NON_PROMOTIONAL"
    PROMOTIONAL_NON_PROMOTIONAL = "BOTH"


CONTENT_TYPE_DICT = {
    ContentType.PROMOTIONAL: [ContentType.PROMOTIONAL],
    ContentType.NON_PROMOTIONAL: [ContentType.NON_PROMOTIONAL],
    ContentType.PROMOTIONAL_NON_PROMOTIONAL: [ContentType.PROMOTIONAL, ContentType.NON_PROMOTIONAL,
                                              ContentType.PROMOTIONAL_NON_PROMOTIONAL]
}
