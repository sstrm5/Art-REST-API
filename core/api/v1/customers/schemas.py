from datetime import datetime
from core.api.v1.questions.schemas import AttemptCustomerInfoSchema
from ninja import Schema


class CreateAndAuthInSchema(Schema):
    email: str
    first_name: str
    last_name: str


class GetAndAuthInSchema(Schema):
    email: str


class AuthOutSchema(Schema):
    message: str


class TokenOutSchema(Schema):
    access_token: str
    refresh_token: str
    expires_in: int


class TokenCreateInSchema(Schema):
    first_name: str
    last_name: str
    email: str
    code: str


class TokenGetInSchema(Schema):
    email: str
    code: str


class RefreshInSchema(Schema):
    refresh_token: str


class UserInfoSchema(Schema):
    id: int
    avatar_path: str
    user_name: str
    user_email: str
    user_created_at: datetime
    user_attempts: list[AttemptCustomerInfoSchema]
