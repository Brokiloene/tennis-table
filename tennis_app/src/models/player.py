from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from tennis_app.src.infrastructure.database import BaseModel


class PlayerModel(BaseModel):
    __tablename__ = "player"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), index=True, unique=True)
