from pydantic import BaseModel


class AccessTokenSchema(BaseModel):
    access_token: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
