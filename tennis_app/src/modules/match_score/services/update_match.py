from typing import Dict
from uuid import UUID

from tennis_app.src.shared.dao import MemoryStorageDAO
from tennis_app.src.shared.core import BaseService
from tennis_app.src.shared.serializers import MatchToDictSerializer
from .save_match import SaveMatchService


class UpdateMatchService(BaseService):
    """
    :raises: MatchNotFoundError
    """

    def execute(match_uuid: UUID, update_info: Dict) -> Dict:
        if update_info == "p1":
            MemoryStorageDAO.update(match_uuid, 1)
        else:
            MemoryStorageDAO.update(match_uuid, 2)

        match_obj = MemoryStorageDAO.read(match_uuid)
        view_data = MatchToDictSerializer.serialize(match_obj)
        if view_data["match_status"] == "match is over":
            SaveMatchService.execute(match_uuid)
        return view_data
