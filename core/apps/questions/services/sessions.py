from abc import ABC, abstractmethod

from core.apps.questions.entities.sessions import Session as SessionEntity
from core.apps.questions.exceptions.questions import SessionAlreadyExistsException
from core.apps.questions.models.sessions import Session as SessionModel


class BaseSessionService:
    @abstractmethod
    def create_session(self, user_id: int, test_id: int) -> SessionEntity:
        ...

    @abstractmethod
    def get_session_by_user_and_test(self, user_id: int, test_id: int) -> SessionEntity:
        ...


class ORMSessionService(BaseSessionService):
    def create_session(self, user_id, test_id) -> SessionEntity:
        if SessionModel.objects.filter(user_id=user_id, test_id=test_id).exists():
            raise SessionAlreadyExistsException()
        session = SessionModel.objects.create(
            user_id=user_id, test_id=test_id)
        return session.to_entity()

    def get_session_by_user_and_test(self, user_id, test_id) -> SessionEntity:
        session = SessionModel.objects.filter(
            user_id=user_id, test_id=test_id).first()
        if not session:
            return None
        return session.to_entity()

    def delete_session_by_user(self, user_id):
        SessionModel.objects.filter(user_id=user_id).delete()
        return True

    def is_session_exists(self, user_id: int):
        return SessionModel.objects.filter(user_id=user_id).exists()

    def find_out_the_current_test(self, user_id: int):
        current_test = SessionModel.objects.filter(user__id=user_id).first()
        print(current_test.test.id)
        if not current_test:
            return -1
        return current_test.test.id
