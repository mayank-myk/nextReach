from string import Template

from app.constants import error_codes
from app.exceptions import Error, GenericException

INVALID_EVENT_PAYLOAD = Error(
    code=error_codes.INVALID_EVENT_PAYLOAD,
    message=Template("Invalid $event_type Event Payload"),
    http_code=500,
)


class InvalidEventPayload(GenericException):
    def __init__(self, ex: Exception, event_id: str, event_type: str) -> None:
        message = INVALID_EVENT_PAYLOAD.message.substitute(event_type=event_type)
        super().__init__(
            message, event_id=event_id, event_type=event_type, ex=ex.__str__()
        )

    @property
    def status_code(self) -> int:
        return INVALID_EVENT_PAYLOAD.http_code

    @property
    def error_code(self) -> str:
        return INVALID_EVENT_PAYLOAD.code
