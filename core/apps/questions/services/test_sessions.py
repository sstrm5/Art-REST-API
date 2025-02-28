from abc import ABC, abstractmethod

from core.apps.questions.entities.test_sessions import TestSession as TestSessionEntity
from core.apps.questions.exceptions.questions import TestSessionAlreadyExistsException
from core.apps.questions.models.test_sessions import TestSession as TestSessionModel


class BaseTestSessionService:
    @abstractmethod
    def create_session(self, user_id: int, test_id: int) -> TestSessionEntity:
        ...

    @abstractmethod
    def get_session_by_user_and_test(self, user_id: int, test_id: int) -> TestSessionEntity:
        ...


class ORMTestSessionService(BaseTestSessionService):
    def create_session(self, user_id, test_id) -> TestSessionEntity:
        if TestSessionModel.objects.filter(user_id=user_id, test_id=test_id).exists():
            raise TestSessionAlreadyExistsException()
        session = TestSessionModel.objects.create(
            user_id=user_id, test_id=test_id)
        return session.to_entity()

    def get_session_by_user_and_test(self, user_id, test_id) -> TestSessionEntity:
        session = TestSessionModel.objects.filter(
            user_id=user_id, test_id=test_id).first()
        if not session:
            return None
        return session.to_entity()

    def delete_session_by_user(self, user_id):
        TestSessionModel.objects.filter(user_id=user_id).delete()
        return True

    def is_session_exists(self, user_id: int):
        return TestSessionModel.objects.filter(user_id=user_id).exists()

    def find_out_the_current_test(self, user_id: int):
        current_test = TestSessionModel.objects.filter(
            user__id=user_id).first()
        if not current_test:
            return -1
        return current_test.test.id
