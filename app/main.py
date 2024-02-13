from fastapi import FastAPI
from app.crud.security.security import router as security_router
from app.crud.table import router as table_router
from app.crud.crud_user import router as user_router
from app.crud.admin import router as admin_router


app = FastAPI()
app.include_router(router=security_router)
app.include_router(router=table_router)
app.include_router(router=user_router)
app.include_router(router=admin_router)
