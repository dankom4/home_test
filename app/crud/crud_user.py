from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Response, Depends, HTTPException
from sqlalchemy import select, update
from passlib.context import CryptContext

from app.db.database import async_session
from app.models.models_for_user import User
from app.schemas.schemas_for_user import UserFull, UserOauth2
import app.crud.security.security as auth
from app.models.models_for_items import Items
from app.schemas.schemas_for_items import ItemsIn


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


@router.post('/user/me/login')
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


@router.patch('/user/me/patch/password')
async def patch_password(current_user: Annotated[User, Depends(auth.get_current_user)],
                         new_passwords: str,
                         response: Response):
    async with async_session() as session:
        usr = await session.execute(select(User).where(User.id == current_user.id))
        user = usr.scalars().first()
        new_password = await auth.get_password_hash(new_passwords)
        user.password = new_password
        response.delete_cookie(key='Authorization')
        await session.flush()
        await session.commit()
        await auth.login_for_access_token(form_data=UserOauth2(username=current_user.email,
                                                               password=new_passwords),
                                          response=response)
        await session.commit()
        return 'new password set'


@router.delete('/user/me/delete')
async def delete_user(current_user: Annotated[User, Depends(auth.get_current_user)], response: Response):
    async with async_session() as session:
        response.delete_cookie(key='Authorization')
        await session.delete(current_user)
        await session.flush()
        await session.commit()
    return f'USER: {current_user.username} DELETE'


@router.get('/user/me/items')
async def show_items(current_user: Annotated[User, Depends(auth.get_current_user)]):
    async with async_session() as session:
        itm = await session.execute(select(Items).where(Items.user_id == current_user.id))
        item = itm.scalars().all()
    return item


@router.post('/user/me/items/add')
async def add_items(current_user: Annotated[User, Depends(auth.get_current_user)],
                    items: ItemsIn):
    async with async_session() as session:
        item = Items(title=items.title, price=items.price, picture=items.picture,
                     specifications=items.specifications, user_id=current_user.id)
        session.add(item)
        await session.flush()
        await session.commit()
    return f'ITEMS: {items.title} CREATED'


@router.delete('/user/me/items/delete')
async def delete_items(current_user: Annotated[User, Depends(auth.get_current_user)],
                       item_id: UUID):
    async with async_session() as session:
        itm = await session.execute(select(Items).where(Items.user_id == current_user.id, Items.id == item_id))
        item = itm.scalars().first()
        if item is None:
            raise HTTPException(status_code=404)
        await session.delete(item)
        await session.flush()
        await session.commit()
    return f'ITEMS: {item_id} DELETE'














