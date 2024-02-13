from pydantic import BaseModel, UUID4


class ItemsFull(BaseModel):
    id: UUID4
    title: str
    price: float
    picture: str
    specifications: str
    user_id: int


class ItemOut(BaseModel):
    title: str
    price: float
    picture: str
    specifications: str
    user_id: int