from dto import CreateMatchDTO
from models import MatchModel
from .base import BaseDAO


class MatchDAO(BaseDAO):
    def insert_one(dto: CreateMatchDTO) -> None:
        with BaseDAO.new_session() as session:
            match_to_add = MatchModel(**dto.asdict())
            session.add(match_to_add)
            session.commit()
    