import fastapi
import jwt
from fastapi import Depends, HTTPException, status, Response, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from passlib.context import CryptContext
from typing import Annotated
from app.db.database import async_session
from sqlalchemy import select
from app.models.models_for_user import User
from app.crud.security.schemas import Token, OAuth2PasswordBearerWithCookieOnly

router = APIRouter(prefix='/auth')
router.include_router(router=router)
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearerWithCookieOnly(tokenUrl='/auth/token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(email: str):
    async with async_session() as session:
        res = await session.execute(select(User).where(User.email == email))
        result = res.scalars().first()
        return result


async def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user:
        return False
    if not await verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email = payload.get('email')
        if email is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)
    user = await get_user(email)
    if user is None:
        raise HTTPException(status_code=401)
    return user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        response: Response
):
    user = await authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_token({'email': form_data.username})
    response.set_cookie(key="Authorization",
                        value="Bearer {}".format(fastapi.encoders.jsonable_encoder(access_token)),
                        httponly=True,)
    return Token(access_token=access_token, token_type='bearer')



