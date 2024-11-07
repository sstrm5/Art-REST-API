from functools import lru_cache
from punq import Container

from core.apps.guide.services.guide import BaseCardService, CardService


@lru_cache(1)
def get_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()

    container.register(BaseCardService, CardService)

    return container
