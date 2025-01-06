from abc import ABC, abstractmethod
import random

from django.core.cache import cache

from core.apps.customers.entities import CustomerEntity
from core.apps.customers.exceptions.codes import CodeNotEqualException, CodeNotFoundException


class BaseCodeService(ABC):
    @abstractmethod
    def generate_code(self, email: str) -> str:
        ...

    @abstractmethod
    def validate_code(self, code: str, email: str) -> None:
        ...


class DjangoCacheCodeService(BaseCodeService):
    def generate_code(self, email: str) -> str:
        code = str(random.randint(100000, 999999))
        cache.set(email, code)
        return code

    def validate_code(self, code: str, email: str) -> None:
        cached_code = cache.get(email)

        if cached_code is None:
            raise CodeNotFoundException(code=code)

        if cached_code != code:
            raise CodeNotEqualException(
                code=code,
                cached_code=cached_code,
                customer_email=email,
            )

        cache.delete(email)
