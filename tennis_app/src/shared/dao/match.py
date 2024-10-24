from typing import List

from sqlalchemy import select, text, func

from tennis_app.src.shared.dto import CreateMatchDTO, ReadMatchDTO
from tennis_app.src.shared.core import BaseDAO
from tennis_app.src.models import MatchModel


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

    def _get_offset(page: int, matches_on_page_cnt: int) -> int:
        if page == 1:
            return 0
        else:
            return matches_on_page_cnt * (page - 1)

    def get_cnt_of_matches(search_name: str | None = None) -> int:
        with BaseDAO.new_session() as session:
            if search_name is None:
                stmt = select(func.count()).select_from(MatchModel)
                res = session.execute(stmt).scalar_one()
            else:
                stmt = text(
                    """
                select COUNT(*)
                from `match` m, player p1, player p2
                where m.player1_id = p1.id and m.player2_id = p2.id and
                (p1.name LIKE :search_query or p2.name LIKE :search_query)
                """
                )
                res = session.execute(
                    stmt, {"search_query": f"%{search_name}%"}
                ).scalar_one()

            return res

    def fetch_all(page: int, matches_on_page_cnt: int) -> List[ReadMatchDTO]:
        matches_data = []
        with BaseDAO.new_session() as session:
            stmt = text(
                """
                select m.score, p1.name, p2.name
                from `match` m, player p1, player p2
                where m.player1_id = p1.id and m.player2_id = p2.id
                order by m.id
                limit :limit
                offset :offset
                """
            )
            limit = matches_on_page_cnt
            offset = MatchDAO._get_offset(page, matches_on_page_cnt)
            matches_data = session.execute(stmt, {"limit": limit, "offset": offset})
        matches_dtos = []
        for score, name1, name2 in matches_data:
            matches_dtos.append(
                ReadMatchDTO(player1_name=name1, player2_name=name2, score=score)
            )
        return matches_dtos

    def fetch_filtered(search_query: str, page: int, matches_on_page_cnt: int):
        matches_data = []
        with BaseDAO.new_session() as session:
            stmt = text(
                """
                select m.score, p1.name, p2.name
                from `match` m, player p1, player p2
                where m.player1_id = p1.id and m.player2_id = p2.id and
                (p1.name LIKE :search_query or p2.name LIKE :search_query)
                order by m.id
                limit :limit
                offset :offset
                """
            )
            limit = matches_on_page_cnt
            offset = MatchDAO._get_offset(page, matches_on_page_cnt)
            matches_data = session.execute(
                stmt,
                {"search_query": f"%{search_query}%", "limit": limit, "offset": offset},
            )
        matches_dtos = []
        for score, name1, name2 in matches_data:
            matches_dtos.append(
                ReadMatchDTO(player1_name=name1, player2_name=name2, score=score)
            )

        return matches_dtos
