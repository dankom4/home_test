from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from uuid import UUID, uuid4

from app.db.database import Base


class Items(Base):
    __tablename__ = 'items'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    picture: Mapped[str]
    specifications: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
