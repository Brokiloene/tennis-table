from typing import List

from sqlalchemy import select

from tennis_app.dto import CreateMatchDTO, ReadMatchDTO
from tennis_app.models import MatchModel, PlayerModel
from .base import BaseDAO


class MatchDAO(BaseDAO):
    def insert_one(dto: CreateMatchDTO) -> None:
        with BaseDAO.new_session() as session:
            match_uuid = dto.uuid
            stmt = select(MatchModel.id).filter_by(uuid=match_uuid)
            result = session.execute(stmt).scalar_one_or_none()
            if result is None:
                match_to_add = MatchModel(**dto.asdict())
                session.add(match_to_add)
                session.commit()

    def fetch_all() -> List[ReadMatchDTO]:
        matches_dtos = []
        with BaseDAO.new_session() as session:
            stmt = select(MatchModel)
            all_matches = session.execute(stmt).scalars().all()
            for match in all_matches:
                p1_name = session.get(PlayerModel, match.player1_id).name
                p2_name = session.get(PlayerModel, match.player2_id).name
                matches_dtos.append(ReadMatchDTO(
                    player1_name=p1_name,
                    player2_name=p2_name,
                    score=match.score
                ))
        print(matches_dtos)
        return matches_dtos
                
