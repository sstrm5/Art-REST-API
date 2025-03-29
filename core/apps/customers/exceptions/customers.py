from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class CustomerException(ServiceException):
    @property
    def message(self):
        return "Customer error occured"


@dataclass(eq=False)
class RefreshTokenNotFoundException(CustomerException):
    @property
    def message(self):
        return "Refresh token not exist"


@dataclass(eq=False)
class RefreshTokenExpiredException(CustomerException):
    @property
    def message(self):
        return "Refresh token is not valid"


@dataclass(eq=False)
class AccessTokenExcpiredException(CustomerException):
    @property
    def message(self):
        return "Access token is not valid"


@dataclass(eq=False)
class CustomerDoesNotExist(CustomerException):
    @property
    def message(self):
        return "Customer not exists"
