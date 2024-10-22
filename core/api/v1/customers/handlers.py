from django.http import HttpRequest
from core.api.v1.questions.schemas import CheckUserExistenceIn, CheckUserExistenceOut
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
from core.apps.customers.services.auth import AuthService
from core.apps.customers.services.codes import DjangoCacheCodeService
from core.apps.customers.services.customers import BaseCustomerService, ORMCustomerService
from core.apps.customers.services.senders import MailSenderService


router = Router(tags=['Customers'])


@router.post('create_and_auth', response=ApiResponse, operation_id='create_and_authorize')
def create_and_auth_handler(request: HttpRequest, schema: CreateAndAuthInSchema) -> ApiResponse:
    service = AuthService(
        customer_service=ORMCustomerService(),
        codes_service=DjangoCacheCodeService(),
        sender_service=MailSenderService(),
    )
    service.create_and_authorize(
        email=schema.email,
        first_name=schema.first_name,
        last_name=schema.last_name,
    )

    return ApiResponse(data=AuthOutSchema(message=f'Code sent to: {schema.email}'))


@router.post('get_and_auth', response=ApiResponse, operation_id='get_and_authorize')
def get_and_auth_handler(request: HttpRequest, schema: GetAndAuthInSchema) -> ApiResponse:
    service = AuthService(
        customer_service=ORMCustomerService(),
        codes_service=DjangoCacheCodeService(),
        sender_service=MailSenderService(),
    )
    service.get_and_authorize(
        email=schema.email,
    )

    return ApiResponse(data=AuthOutSchema(message=f'Code sent to: {schema.email}'))


@router.post('confirm', response=ApiResponse, operation_id='confirm')
def get_token_handler(request: HttpRequest, schema: TokenInSchema) -> ApiResponse:
    service = AuthService(
        customer_service=ORMCustomerService(),
        codes_service=DjangoCacheCodeService(),
        sender_service=MailSenderService(),
    )
    try:
        access_token, refresh_token, expires_in = service.confirm(
            email=schema.email, code=schema.code,)
    except ServiceException as exception:
        raise HttpError(status_code=400,
                        message=exception.message) from exception

    return ApiResponse(data=TokenOutSchema(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in))


@router.post('refresh', response=ApiResponse, operation_id='refresh')
def refresh_token_handler(request: HttpRequest, schema: RefreshInSchema) -> ApiResponse:
    service = ORMCustomerService()
    try:
        access_token, refresh_token, expires_in = service.refresh_token(
            refresh_token=schema.refresh_token)
    except ServiceException as exception:
        raise HttpError(status_code=400,
                        message=exception.message) from exception

    return ApiResponse(data=TokenOutSchema(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in))


@router.post('/check/user_existence', response=ApiResponse)
def check_user_existence_handler(
    request,
    schema: CheckUserExistenceIn,
) -> ApiResponse:
    try:
        customer_service: BaseCustomerService = ORMCustomerService()
        is_user_exists = customer_service.check_user_existence(
            email=schema.email)

        return ApiResponse(data=CheckUserExistenceOut(is_user_exists=is_user_exists))
    except Exception as exception:
        raise HttpError(status_code=400, message=exception.message)
