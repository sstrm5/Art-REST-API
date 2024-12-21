from django.http import HttpRequest
from core.api.v1.questions.schemas import CheckUserExistenceIn, CheckUserExistenceOut
from core.apps.questions.containers import get_container
from ninja import Router
from ninja.errors import HttpError

from core.api.schemas import ApiResponse
from core.api.v1.customers.schemas import (
    AuthOutSchema,
    CreateAndAuthInSchema,
    GetAndAuthInSchema,
    RefreshInSchema,
    TokenInSchema,
    TokenOutSchema,
)
from core.apps.common.exceptions import ServiceException
from core.apps.customers.services.auth import BaseAuthService
from core.apps.customers.services.customers import BaseCustomerService


router = Router(tags=['Customers👨‍💻'])


@router.post('create_and_auth', response=ApiResponse[AuthOutSchema], operation_id='create_and_authorize', summary='Создать пользователя и отправить код✉️')
def create_and_auth_handler(request: HttpRequest, schema: CreateAndAuthInSchema) -> ApiResponse:
    container = get_container()
    service = container.resolve(BaseAuthService)
    service.create_and_authorize(
        email=schema.email,
        first_name=schema.first_name,
        last_name=schema.last_name,
    )

    return ApiResponse(data=AuthOutSchema(message=f'Code sent to: {schema.email}'))


@router.post('get_and_auth', response=ApiResponse[AuthOutSchema], operation_id='get_and_authorize', summary='Получить пользователя и отправить код✉️')
def get_and_auth_handler(request: HttpRequest, schema: GetAndAuthInSchema) -> ApiResponse:
    container = get_container()
    service = container.resolve(BaseAuthService)
    service.get_and_authorize(
        email=schema.email,
    )

    return ApiResponse(data=AuthOutSchema(message=f'Code sent to: {schema.email}'))


@router.post('confirm', response=ApiResponse[TokenOutSchema], operation_id='confirm', summary='Проверить код и получить токены✅')
def get_token_handler(request: HttpRequest, schema: TokenInSchema) -> ApiResponse:
    container = get_container()
    service = container.resolve(BaseAuthService)
    try:
        access_token, refresh_token, expires_in = service.confirm(
            email=schema.email, code=schema.code,)
    except ServiceException as exception:
        raise HttpError(status_code=400,
                        message=exception.message) from exception

    return ApiResponse(data=TokenOutSchema(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in))


@router.post('refresh', response=ApiResponse[TokenOutSchema], operation_id='refresh', summary='Обновить токены*️⃣')
def refresh_token_handler(request: HttpRequest, schema: RefreshInSchema) -> ApiResponse:
    container = get_container()
    service = container.resolve(BaseCustomerService)
    try:
        access_token, refresh_token, expires_in = service.refresh_token(
            refresh_token=schema.refresh_token)
    except ServiceException as exception:
        raise HttpError(status_code=400,
                        message=exception.message) from exception

    return ApiResponse(data=TokenOutSchema(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in))


@router.post('/check/user_existence', response=ApiResponse[CheckUserExistenceOut], summary='Проверить существование пользователя🧙‍♂️')
def check_user_existence_handler(
    request,
    schema: CheckUserExistenceIn,
) -> ApiResponse:
    try:
        container = get_container()
        customer_service = container.resolve(BaseCustomerService)
        is_user_exists = customer_service.check_user_existence(
            email=schema.email)

        return ApiResponse(data=CheckUserExistenceOut(is_user_exists=is_user_exists))
    except Exception as exception:
        raise HttpError(status_code=400, message=exception.message)
