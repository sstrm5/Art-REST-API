from abc import ABC, abstractmethod
import time
from uuid import uuid4

from core.apps.customers.entities import CustomerEntity
from core.apps.customers.exceptions.customers import RefreshTokenExpiredException, RefreshTokenNotFoundException
from core.apps.customers.models import Customer


class BaseCustomerService(ABC):
    @abstractmethod
    def get_or_create(self, phone: str) -> CustomerEntity:
        ...
    
    @abstractmethod
    def get(self, phone: str) -> CustomerEntity:
        ...

    @abstractmethod
    def generate_token(self, customer: CustomerEntity) -> str:
        ...

class ORMCustomerService(BaseCustomerService):
    def get_or_create(self, phone: str) -> CustomerEntity:
        customer, _ = Customer.objects.get_or_create(phone=phone)

        return customer.to_entity()
    
    def get(self, phone: str) -> CustomerEntity:
        customer = Customer.objects.get(phone=phone)

        return customer.to_entity()
    
    def generate_token(self, customer: CustomerEntity) -> tuple:
        new_access_token = str(uuid4())
        new_refresh_token = str(uuid4())
        current_time = int(time.time())
        expires_in = current_time + 3600
        refresh_expires_in = current_time + 604800
        Customer.objects.filter(phone=customer.phone).update(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=expires_in,
            refresh_expires_in=refresh_expires_in,
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
                refresh_expires_in = current_time + 604800
                Customer.objects.filter(phone=customer.phone).update(
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
