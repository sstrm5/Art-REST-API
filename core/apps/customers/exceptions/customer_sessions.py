from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class SessionDoesNotExistException(ServiceException):
    @property
    def message(self):
        return 'Session does not exist (user is not authorized)'
