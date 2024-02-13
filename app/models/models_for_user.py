from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.models_for_items import Items

from app.db.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False, default='user')
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    items: Mapped[list['Items']] = relationship(backref='items', passive_deletes=True)
