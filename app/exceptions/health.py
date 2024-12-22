from app.constants import error_codes
from app.exceptions import Error, GenericException

SERVER_NOT_HEALTHY = Error(
    code=error_codes.SERVER_NOT_HEALTHY, message="Health - Not OK", http_code=503
)


class ServerNotHealthyException(GenericException):
    def __init__(self, failed_entity: str) -> None:
        super().__init__(SERVER_NOT_HEALTHY.message, failed_entity=failed_entity)

    @property
    def error_code(self) -> str:
        return SERVER_NOT_HEALTHY.code

    @property
    def status_code(self) -> int:
        return SERVER_NOT_HEALTHY.http_code
