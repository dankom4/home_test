from fastapi import APIRouter, Response
from passlib.context import CryptContext
from sqlalchemy import select

from app.db.database import async_session
from app.models.models_for_user import User
from app.schemas.schemas_for_user import UserFull, UserOauth2
import app.crud.security.security as auth


router = APIRouter(prefix='/admin', tags=['ADMIN'])


@router.post('/show_all_user')
async def show_all_user():
    async with async_session() as session:
        res = await session.execute(select(User))
        result = res.scalars().all()
        return result
