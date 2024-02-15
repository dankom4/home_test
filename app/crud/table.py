from fastapi import APIRouter

from app.db.database import engine, Base, engine_docker


router = APIRouter(prefix='/table')


@router.post('/create_table', tags=['TABLE'])
async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@router.post('/drop_table', tags=['TABLE'])
async def drop_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@router.post('/create_table_docker', tags=['DOCKER'])
async def create_table_docker():
    async with engine_docker.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@router.post('/drop_table_docker', tags=['DOCKER'])
async def drop_table_docker():
    async with engine_docker.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
