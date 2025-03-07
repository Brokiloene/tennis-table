from uuid import UUID

from tennis_app.src.shared.dao import MemoryStorageDAO
from tennis_app.src.shared.core import BaseService
from tennis_app.src.shared.serializers import MatchToDictSerializer
from tennis_app.src.shared.tennis_game_logic import Match
from .save_match import SaveMatchService


class UpdateMatchService(BaseService):
    """
    :raises: MatchNotFoundError
    """

    @staticmethod
    def execute(match_uuid: UUID, update_info: str) -> dict[str, str]:
        if update_info == "p1":
            MemoryStorageDAO.update(match_uuid, 1)
        else:
            MemoryStorageDAO.update(match_uuid, 2)

        match_: Match = MemoryStorageDAO.read(match_uuid)
        view_data: dict[str, str] = MatchToDictSerializer.serialize(match_)
        if view_data["match_status"] == "match is over":
            SaveMatchService.execute(match_uuid)
        return view_data
