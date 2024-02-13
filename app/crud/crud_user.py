from typing import Annotated

from fastapi import APIRouter, Response, Depends
from passlib.context import CryptContext
from sqlalchemy import select

from app.db.database import async_session
from app.models.models_for_user import User
from app.schemas.schemas_for_user import UserFull, UserOauth2
import app.crud.security.security as auth


router = APIRouter(prefix='/user', tags=['USER'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/sing_up')
async def sing_up(users: UserFull, response: Response):
    async with async_session() as session:
        password = await auth.get_password_hash(users.password)
        user = User(username=users.username, password=password, email=users.email)
        session.add(user)
        await session.flush()
        await session.commit()
        await auth.login_for_access_token(form_data=UserOauth2(username=users.email, password=users.password),
                                          response=response)
        return f'USER: {users.username.upper()} CREATED'


@router.post('/login')
async def login_user(users: UserFull, response: Response):
    await auth.login_for_access_token(form_data=UserOauth2(username=users.email, password=users.password),
                                      response=response)
    return f'USER: {users.username.upper()} LOGIN'


@router.post("/user/me/logout")
async def logout(
    current_user: Annotated[User, Depends(auth.get_current_user)],
        response: Response
):
    response.delete_cookie(key='Authorization')
    return F"USER: {current_user.username} LOGOUT"


@router.get('/user/me')
async def read_me(current_user: Annotated[User, Depends(auth.get_current_user)]):
    return current_user
















