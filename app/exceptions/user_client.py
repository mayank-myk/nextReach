from app.constants import error_codes
from app.exceptions import Error, GenericException

USER_CLIENT_GENERIC_ERROR = Error(
    code=error_codes.USER_CLIENT_GENERIC_ERROR,
    message="Generic client exception",
    http_code=422,
)

USER_NOT_FOUND = Error(
    code=error_codes.USER_NOT_FOUND,
    message="User Not Found",
    http_code=404,
)

USER_PHONE_NUMBER_NOT_FOUND = Error(
    code=error_codes.USER_PHONE_NUMBER_NOT_FOUND,
    message="User Phone number missing",
    http_code=500,
)


class UserClientGenericException(GenericException):
    def __init__(self, ex: Exception, user_id: str, endpoint: str) -> None:
        message = USER_CLIENT_GENERIC_ERROR.message
        super().__init__(message, user_id=user_id, endpoint=endpoint, ex=str(ex))

    @property
    def status_code(self) -> int:
        return USER_CLIENT_GENERIC_ERROR.http_code

    @property
    def error_code(self) -> str:
        return USER_CLIENT_GENERIC_ERROR.code


class UserNotFound(GenericException):
    def __init__(self, user_id: str, endpoint: str) -> None:
        message = USER_NOT_FOUND.message
        super().__init__(message, user_id=user_id, endpoint=endpoint)

    @property
    def status_code(self) -> int:
        return USER_NOT_FOUND.http_code

    @property
    def error_code(self) -> str:
        return USER_NOT_FOUND.code


class UserPhoneNumberNotFound(GenericException):
    def __init__(self, user_id: str, endpoint: str) -> None:
        message = USER_PHONE_NUMBER_NOT_FOUND.message
        super().__init__(message, user_id=user_id, endpoint=endpoint)

    @property
    def status_code(self) -> int:
        return USER_PHONE_NUMBER_NOT_FOUND.http_code

    @property
    def error_code(self) -> str:
        return USER_PHONE_NUMBER_NOT_FOUND.code
