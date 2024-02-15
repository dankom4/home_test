from fastapi import APIRouter
from sqlalchemy import select

from app.db.database import async_session
from app.models.models_for_items import Items
from app.models.models_for_user import User


router = APIRouter(prefix='/admin', tags=['ADMIN'])


@router.post('/show_all_user')
async def show_all_user():
    async with async_session() as session:
        res = await session.execute(select(User))
        result = res.scalars().all()
        return result


@router.post('/show_all_items')
async def show_all_items():
    async with async_session() as session:
        res = await session.execute(select(Items))
        result = res.scalars().all()
        return result
