import requests.exceptions



class ApiException(Exception):
    pass


class HttpCodeException(ApiException):
    pass


class IncorrectTokenException(ApiException):
    STATUS = "E_24"

class MethodAccessException(ApiException):
    STATUS = "E_23"

class MethodNotFoundException(ApiException):
    STATUS = "E_2"


API_EXCEPTIONS = (IncorrectTokenException, MethodAccessException, MethodNotFoundException)