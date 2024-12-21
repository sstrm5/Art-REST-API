from dataclasses import dataclass

from core.apps.common.exceptions import ServiceException


@dataclass(eq=False)
class CreateException(ServiceException):
    @property
    def message(self):
        return 'Create test error occured'


@dataclass(eq=False)
class SubjectException(CreateException):
    @property
    def message(self):
        return 'Subject error occured'


@dataclass(eq=False)
class QuestionException(CreateException):
    @property
    def message(self):
        return 'Question error occured'


@dataclass(eq=False)
class WrongAccessTokenException(CreateException):
    @property
    def message(self):
        return 'Invalid access token'


@dataclass(eq=False)
class TestNotFoundException(ServiceException):
    @property
    def message(self):
        return 'Test not found'


@dataclass(eq=False)
class TestAlreadyStartedException(ServiceException):
    @property
    def message(self):
        return 'Test already started'
