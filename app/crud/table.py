from passlib.context import CryptContext

from app.db.database import engine, Base, async_session
from fastapi import APIRouter
from app.models.models_for_user import User
from app.schemas.schemas_for_user import UserFull


router = APIRouter(prefix='/table', tags=['TABLE'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_password_hash(password):
    return pwd_context.hash(password)


@router.post('/create_table')
async def table_create():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@router.post('/drop')
async def drop():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
