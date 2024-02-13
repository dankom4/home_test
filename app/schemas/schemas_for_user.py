from pydantic import BaseModel, EmailStr

from app.schemas.schemas_for_items import ItemsFull


class UserFull(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = 'user'
    is_active: bool = True
    items: list['ItemsFull'] = []


class UserOauth2(BaseModel):
    grant_type: str | None = None
    username: str | EmailStr
    password: str
    scopes: list = []
    client_id: str | None = None
    client_secret: str | None = None


class UserOut(BaseModel):
    username: str
    email: str
    role: str
    items: list['ItemsFull'] = []
