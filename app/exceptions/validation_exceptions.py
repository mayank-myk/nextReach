from string import Template

from app.constants import error_codes
from app.exceptions import Error, GenericException

INVALID_PHONE_NUMBER_ERROR = Error(
    code=error_codes.INVALID_PHONE_NUMBER_ERROR,
    message=Template(
        "Phone number $phone_number is not valid. It should only contain numbers and 10 characters."
    ),
    http_code=422,
)

EMPTY_PHONE_NUMBERS_LIST_ERROR = Error(
    code=error_codes.EMPTY_PHONE_NUMBERS_LIST_ERROR,
    message="The phone_numbers list cannot be an empty",
    http_code=422,
)

EXCEED_PHONE_NUMBERS_LIST_LENGTH_ERROR = Error(
    code=error_codes.EXCEED_PHONE_NUMBERS_LIST_LENGTH_ERROR,
    message=Template("The phone_numbers list cannot have a size more than $max_length"),
    http_code=422,
)

MISSING_REQUIRED_FIELD = Error(
    code=error_codes.MISSING_REQUIRED_FIELD_ERROR,
    message=Template("Missing Required Field: $field"),
    http_code=422,
)


class MissingRequiredField(GenericException):
    def __init__(self, field: str) -> None:
        message = MISSING_REQUIRED_FIELD.message.substitute(field=field)
        super().__init__(message, field=field)

    @property
    def status_code(self) -> int:
        return MISSING_REQUIRED_FIELD.http_code

    @property
    def error_code(self) -> str:
        return MISSING_REQUIRED_FIELD.code

    @property
    def should_notify(self) -> bool:
        return False


class InvalidPhoneNumberException(GenericException):
    def __init__(self, phone_number: str) -> None:
        message = INVALID_PHONE_NUMBER_ERROR.message.substitute(
            phone_number=phone_number
        )
        super().__init__(message, phone_number=phone_number)

    @property
    def status_code(self) -> int:
        return INVALID_PHONE_NUMBER_ERROR.http_code

    @property
    def error_code(self) -> str:
        return INVALID_PHONE_NUMBER_ERROR.code

    @property
    def should_notify(self) -> bool:
        return False


class EmptyPhoneNumbersListException(GenericException):
    def __init__(self) -> None:
        message = EMPTY_PHONE_NUMBERS_LIST_ERROR.message
        super().__init__(message)

    @property
    def status_code(self) -> int:
        return EMPTY_PHONE_NUMBERS_LIST_ERROR.http_code

    @property
    def error_code(self) -> str:
        return EMPTY_PHONE_NUMBERS_LIST_ERROR.code

    @property
    def should_notify(self) -> bool:
        return False


class ExceedPhoneNumbersListLengthException(GenericException):
    def __init__(self, max_length: int) -> None:
        message = EXCEED_PHONE_NUMBERS_LIST_LENGTH_ERROR.message.substitute(
            max_length=max_length
        )
        super().__init__(message)

    @property
    def status_code(self) -> int:
        return EXCEED_PHONE_NUMBERS_LIST_LENGTH_ERROR.http_code

    @property
    def error_code(self) -> str:
        return EXCEED_PHONE_NUMBERS_LIST_LENGTH_ERROR.code

    @property
    def should_notify(self) -> bool:
        return False
