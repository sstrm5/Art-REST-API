from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from core.api.schemas import ApiResponse
from core.api.v1.customers.schemas import (
    AuthInSchema,
    AuthOutSchema,
    RefreshInSchema,
    TokenInSchema,
    TokenOutSchema,
)
from core.apps.common.exceptions import ServiceException
from core.apps.customers.services.auth import AuthService
from core.apps.customers.services.codes import DjangoCacheCodeService
from core.apps.customers.services.customers import ORMCustomerService
from core.apps.customers.services.senders import DummySenderService


router = Router(tags=['Customers'])

@router.post('auth', response=ApiResponse[AuthOutSchema], operation_id='authorize')
def auth_handler(request: HttpRequest, schema: AuthInSchema) -> ApiResponse[AuthOutSchema]:
    service = AuthService(
        customer_service=ORMCustomerService(),
        codes_service=DjangoCacheCodeService(),
        sender_service=DummySenderService(),
    )
    service.authorize(phone=schema.phone)
    
    return ApiResponse(data=AuthOutSchema(message=f'Code sent to: {schema.phone}'))


@router.post('confirm', response=ApiResponse[TokenOutSchema], operation_id='confirm')
def get_token_handler(request: HttpRequest, schema: TokenInSchema) -> ApiResponse[TokenOutSchema]:
    service = AuthService(
        customer_service=ORMCustomerService(),
        codes_service=DjangoCacheCodeService(),
        sender_service=DummySenderService(),
    )
    try:
        access_token, refresh_token, expires_in = service.confirm(phone=schema.phone, code=schema.code,)
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message) from exception

    return ApiResponse(data=TokenOutSchema(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in))


@router.post('refresh', response=ApiResponse[TokenOutSchema], operation_id='refresh')
def refresh_token_handler(request: HttpRequest, schema: RefreshInSchema) -> ApiResponse[TokenOutSchema]:
    service = ORMCustomerService()
    try:
        access_token, refresh_token, expires_in = service.refresh_token(refresh_token=schema.refresh_token)
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message) from exception

    return ApiResponse(data=TokenOutSchema(access_token=access_token, refresh_token=refresh_token, expires_in=expires_in))
