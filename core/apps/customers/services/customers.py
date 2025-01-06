from abc import ABC, abstractmethod
import time
from uuid import uuid4

from core.apps.customers.customer_session_model import CustomerSession
from core.apps.customers.entities import CustomerEntity
from core.apps.customers.exceptions.customer_sessions import SessionDoesNotExistException
from core.apps.customers.exceptions.customers import AccessTokenExcpiredException, RefreshTokenExpiredException, RefreshTokenNotFoundException
from core.apps.customers.models import Customer


class BaseCustomerService(ABC):
    @abstractmethod
    def get_or_create(self, email: str, first_name: str, last_name: str) -> CustomerEntity:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> CustomerEntity:
        ...

    @abstractmethod
    def generate_token(self, customer: CustomerEntity) -> str:
        ...


class ORMCustomerService(BaseCustomerService):
    def get_or_create(self, email: str, first_name: str, last_name: str) -> CustomerEntity:
        customer, _ = Customer.objects.get_or_create(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        return customer.to_entity()

    def get_by_email(self, email: str) -> CustomerEntity:
        customer = Customer.objects.get(email=email)
        return customer.to_entity()

    def get_by_token(self, token: str, device_info: str) -> CustomerEntity:
        session = CustomerSession.objects.filter(
            access_token=token, device_info=device_info).first()
        if session:
            customer = session.customer
            current_time = int(time.time())
            if current_time < session.expires_in:
                return customer.to_entity()
            raise AccessTokenExcpiredException()
        raise SessionDoesNotExistException()

    def get_by_id(self, user_id: int) -> CustomerEntity:
        customer = Customer.objects.get(id=user_id)
        return customer.to_entity()

    def check_user_existence(self, email: str):
        return Customer.objects.filter(email=email).exists()

    def generate_token(self, customer: CustomerEntity, device_info: str) -> tuple:
        new_access_token = str(uuid4())
        new_refresh_token = str(uuid4())
        current_time = int(time.time())
        expires_in = current_time + 3600
        refresh_expires_in = current_time + 604800
        customer_model = Customer.objects.get(email=customer.email)
        CustomerSession.objects.create(
            customer=customer_model,
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=expires_in,
            refresh_expires_in=refresh_expires_in,
            device_info=device_info,
        )
        return new_access_token, new_refresh_token, expires_in

    def refresh_token(self, refresh_token: str):
        customer = Customer.objects.get(refresh_token=refresh_token)
        if customer:
            current_time = int(time.time())
            if current_time < customer.refresh_expires_in:
                new_access_token = str(uuid4())
                new_refresh_token = str(uuid4())
                expires_in = current_time + 3600
                refresh_expires_in = current_time + 1209600
                Customer.objects.filter(email=customer.email).update(
                    access_token=new_access_token,
                    refresh_token=new_refresh_token,
                    expires_in=expires_in,
                    refresh_expires_in=refresh_expires_in,
                )
                return new_access_token, new_refresh_token, expires_in
            else:
                raise RefreshTokenExpiredException()
        else:
            raise RefreshTokenNotFoundException()

    def change_status(self, customer: CustomerEntity, in_process: bool):
        Customer.objects.filter(email=customer.email).update(
            in_process=in_process)
        return customer.in_process
