from uuid import UUID

from tennis_app.src.shared.dao import PlayerDAO, MatchDAO, MemoryStorageDAO
from tennis_app.src.shared.dto import CreateMatchDTO
from tennis_app.src.shared.core import BaseService
from tennis_app.src.shared.exceptions import MatchNotFoundError
from tennis_app.src.shared.serializers import MatchToDictSerializer
from tennis_app.src.shared.tennis_game_logic import Match


class SaveMatchService(BaseService):
    @staticmethod
    def execute(match_uuid: UUID):
        """
        :raises: MatchNotFoundError
        """
        match_: Match = MemoryStorageDAO.read(match_uuid)
        match_result: str = MatchToDictSerializer.get_only_result_data(match_)

        p1_id: int = PlayerDAO.insert_one(match_.p1_name)
        p2_id: int = PlayerDAO.insert_one(match_.p2_name)

        if match_.p1_name == match_.winner:
            winner_id: int = p1_id
        else:
            winner_id = p2_id

        dto = CreateMatchDTO(
            uuid=str(match_uuid),
            player1_id=p1_id,
            player2_id=p2_id,
            winner_id=winner_id,
            score=match_result,
        )
        MatchDAO.insert_one(dto)
        try:
            MemoryStorageDAO.delete(match_uuid)
        except KeyError:
            raise MatchNotFoundError
