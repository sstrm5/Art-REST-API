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


@dataclass(eq=False)
class TestWasNotStartedException(ServiceException):
    @property
    def message(self):
        return 'Test was not started'


@dataclass(eq=False)
class TestSessionAlreadyExistsException(ServiceException):
    @property
    def message(self):
        return 'The user is already solving the test'


@dataclass(eq=False)
class TestSessionDoesNotExistException(ServiceException):
    @property
    def message(self):
        return 'Test-session does not exist (test was not started)'


@dataclass(eq=False)
class TestSessionNotOverException(ServiceException):
    @property
    def message(self):
        return 'Test-session is not over yet'


@dataclass(eq=False)
class AttemptDoesNotExistException(ServiceException):
    @property
    def message(self):
        return 'Attempt does not exist'


@dataclass(eq=False)
class WrongTestException(ServiceException):
    @property
    def message(self):
        return 'Wrong test id'
