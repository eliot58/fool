class InitDataError(Exception):
    pass


class AuthDateMissingError(InitDataError):
    pass


class SignMissingError(InitDataError):
    pass


class SignInvalidError(InitDataError):
    pass


class UnexpectedFormatError(InitDataError):
    pass


class ExpiredError(InitDataError):
    pass