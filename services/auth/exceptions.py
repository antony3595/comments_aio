from services.common.exceptions import BaseServiceException


class AuthorizationServiceException(BaseServiceException):
    default_message = "Authorization ServiceException"


class AuthorizationException(AuthorizationServiceException):
    default_message = "Authorization Exception"


class AuthenticationException(AuthorizationServiceException):
    default_message = "Authentication Exception"
