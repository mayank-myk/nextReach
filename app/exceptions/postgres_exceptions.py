from app.constants import error_codes
from app.exceptions import Error, GenericException

PSQL_CONNECTION_POLL_ERROR = Error(
    code=error_codes.PSQL_CONNECTION_POLL_ERROR,
    message="PostgresDB Connection Pool Init Error",
    http_code=500,
)
PSQL_CONNECTION_ERROR = Error(
    code=error_codes.PSQL_CONNECTION_ERROR,
    message="PostgresDB Connection Error",
    http_code=500,
)


class ConnectionPoolException(GenericException):
    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message, **kwargs)

    @property
    def error_code(self) -> str:
        return PSQL_CONNECTION_POLL_ERROR.code


class ConnectionException(GenericException):
    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message, **kwargs)

    @property
    def error_code(self) -> str:
        return PSQL_CONNECTION_ERROR.code
