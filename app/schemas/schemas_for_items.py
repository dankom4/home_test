from pydantic import BaseModel, UUID4


class ItemsFull(BaseModel):
    title: str
    price: float
    picture: str
    specifications: str
    user_id: int


class ItemsOut(BaseModel):
    id: UUID4
    title: str
    price: float
    picture: str
    specifications: str
    user_id: int


class ItemsIn(BaseModel):
    title: str
    price: float
    picture: str
    specifications: str
