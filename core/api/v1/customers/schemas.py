from ninja import Schema


class AuthInSchema(Schema):
    phone: str


class AuthOutSchema(Schema):
    message: str


class TokenOutSchema(Schema):
    access_token: str
    refresh_token: str
    expires_in: int


class TokenInSchema(Schema):
    phone: str
    code: str


class RefreshInSchema(Schema):
    refresh_token: str