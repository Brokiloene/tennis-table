# from typing import List
from sqlalchemy import select

from tennis_app.src.models import PlayerModel
from tennis_app.src.shared.exceptions import PlayerNotFoundError
from tennis_app.src.shared.dto import ReadPlayerDTO

from tennis_app.src.shared.core import PersistentDatabaseDAO


class PlayerDAO(PersistentDatabaseDAO):
    @staticmethod
    def insert_one(name: str) -> int:
        with PersistentDatabaseDAO.new_session() as session:
            player = PlayerModel(name=name)
            stmt = select(PlayerModel.id).filter_by(name=name)
            player.id = session.execute(stmt).scalar_one_or_none()  # type: ignore
            if player.id is None:
                session.add(player)
            session.commit()
        return player.id

    @staticmethod
    def select_one_by_name(name: str) -> ReadPlayerDTO:
        """
        :raises: PlayerNotFoundError
        """
        with PersistentDatabaseDAO.new_session() as session:
            stmt = select(PlayerModel).filter_by(name=name)
            player: PlayerModel | None = session.execute(stmt).scalar()
        if player is None:
            raise PlayerNotFoundError(f"Player {name} not found")
        else:
            return ReadPlayerDTO(p_id=player.id, name=player.name)
