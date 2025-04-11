import os
from abc import ABC, abstractmethod
import time
from uuid import uuid4

from ninja import UploadedFile

from core.apps.customers.customer_session_model import CustomerSession
from core.apps.customers.entities import CustomerEntity
from core.apps.customers.exceptions.customer_sessions import (
    SessionDoesNotExistException,
)
from core.apps.customers.exceptions.customers import (
    AccessTokenExcpiredException,
    RefreshTokenExpiredException,
    RefreshTokenNotFoundException,
    CustomerDoesNotExist,
)
from core.apps.customers.image import compress_image
from core.apps.customers.models import Customer


class BaseCustomerService(ABC):
    @abstractmethod
    def get_or_create(
        self, email: str, first_name: str, last_name: str
    ) -> CustomerEntity: ...
    @abstractmethod
    def get_by_email(self, email: str) -> CustomerEntity: ...
    @abstractmethod
    def generate_token(self, customer: CustomerEntity, device_info: str) -> str: ...
    def get_by_token_and_device(self, token, device_info): ...
    def get_by_token(self, token): ...
    def change_avatar(self, customer, avatar_path): ...
    def change_name(self, customer, first_name, last_name): ...
    def save_avatar(self, image_file, customer): ...


class ORMCustomerService(BaseCustomerService):
    def get_or_create(
        self, email: str, first_name: str, last_name: str
    ) -> CustomerEntity:
        customer, _ = Customer.objects.get_or_create(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        return customer.to_entity()

    def get_by_email(self, email: str) -> CustomerEntity:
        customer = Customer.objects.get(email=email)
        return customer.to_entity()

    def get_by_token_and_device(self, token: str, device_info: str) -> CustomerEntity:
        session = CustomerSession.objects.filter(
            access_token=token, device_info=device_info
        ).first()
        if session:
            customer = session.customer
            current_time = int(time.time())
            if current_time < session.expires_in:
                return customer.to_entity()
            raise AccessTokenExcpiredException()
        raise SessionDoesNotExistException()

    def get_by_token(self, token: str):
        session = CustomerSession.objects.filter(access_token=token).first()
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

    def refresh_token(self, refresh_token: str, device_info: str):
        session = CustomerSession.objects.filter(
            refresh_token=refresh_token, device_info=device_info
        ).first()
        if session:
            current_time = int(time.time())
            if current_time < session.refresh_expires_in:
                new_access_token = str(uuid4())
                new_refresh_token = str(uuid4())
                expires_in = current_time + 3600
                refresh_expires_in = current_time + 1209600

                session.access_token = new_access_token
                session.refresh_token = new_refresh_token
                session.expires_in = expires_in
                session.refresh_expires_in = refresh_expires_in

                session.save()
                return new_access_token, new_refresh_token, expires_in
            else:
                raise RefreshTokenExpiredException()
        else:
            raise RefreshTokenNotFoundException()

    def change_status(self, customer: CustomerEntity, in_process: bool):
        Customer.objects.filter(email=customer.email).update(in_process=in_process)
        return customer.in_process

    def save_avatar(self, image_file: UploadedFile, customer: CustomerEntity):
        # создание папки с аватарками, если нет
        if not os.path.exists("media/customers"):
            os.makedirs("media/customers")

        # парсинг расширения
        extension = image_file.name.split(".")[-1]
        if extension.lower() == "jpg":
            extension = "jpeg"

        # создание нового имени файла
        timestamp = int(time.time())
        new_filename = f"{customer.id}?{timestamp}"
        new_file_path = f"customers/{new_filename}.{extension}"

        with open(f"media/{new_file_path}", "wb") as f:
            for chunk in image_file.chunks():
                f.write(chunk)
        compress_image(path=f"media/{new_file_path}", extension=extension)
        return new_file_path

    def change_avatar(self, customer: CustomerEntity, avatar_path: str):
        customer = Customer.objects.filter(id=customer.id).first()
        if not customer:
            raise CustomerDoesNotExist()
        customer.picture = avatar_path
        customer.save()

    def change_name(self, customer: CustomerEntity, first_name: str, last_name: str):
        customer = Customer.objects.filter(id=customer.id).first()
        if not customer:
            raise CustomerDoesNotExist()
        if first_name:
            customer.first_name = first_name
        if last_name:
            customer.last_name = last_name
        customer.save()
