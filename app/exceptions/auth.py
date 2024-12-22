from app.constants import error_codes
from app.exceptions import Error, GenericException

NOT_AUTHORIZED_REQUEST = Error(
    code=error_codes.NOT_AUTHORIZED_REQUEST, message="Not Authorized", http_code=401
)


class NotAuthorizedRequestException(GenericException):
    def __init__(self, service_id: str, nonce: str, signature: str) -> None:
        super().__init__(
            NOT_AUTHORIZED_REQUEST.message,
            service_id=service_id,
            nonce=nonce,
            signature=signature,
        )

    @property
    def error_code(self) -> str:
        return NOT_AUTHORIZED_REQUEST.code

    @property
    def status_code(self) -> int:
        return NOT_AUTHORIZED_REQUEST.http_code
