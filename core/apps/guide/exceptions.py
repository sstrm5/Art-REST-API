from dataclasses import dataclass
from core.apps.common.exceptions import ServiceException


class CardDoesNotExistException(ServiceException):
    @property
    def message(self):
        return "Card does not exist"
