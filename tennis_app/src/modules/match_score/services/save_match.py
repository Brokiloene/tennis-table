from uuid import UUID

from tennis_app.src.shared.dao import PlayerDAO, MatchDAO, MemoryStorageDAO
from tennis_app.src.shared.dto import CreateMatchDTO
from tennis_app.src.shared.core import BaseService
from tennis_app.src.shared.exceptions import MatchNotFoundError
from tennis_app.src.shared.serializers import MatchToDictSerializer

class SaveMatchService(BaseService):   
    def execute(match_uuid: UUID):
        """
        :raises: MatchNotFoundError
        """
        match_obj = MemoryStorageDAO.read(match_uuid)
        match_result = MatchToDictSerializer.get_only_result_data(match_obj)
        match_result = match_obj.get_result_data()
        p1_id = PlayerDAO.insert_one(match_obj.p1_name)
        p2_id = PlayerDAO.insert_one(match_obj.p2_name)

        # p1_id = PlayerDAO.select_one_by_name(p1_name).p_id
        # p2_id = PlayerDAO.select_one_by_name(p2_name).p_id
        if match_obj.p1_name == match_obj.winner:
            winner_id = p1_id
        else:
            winner_id = p2_id
        
        dto = CreateMatchDTO(
            uuid=str(match_uuid), 
            player1_id=p1_id, 
            player2_id=p2_id, 
            winner_id=winner_id, 
            score=match_result
        )
        MatchDAO.insert_one(dto)
        try:
            MemoryStorageDAO.delete(match_uuid)
        except KeyError:
            raise MatchNotFoundError

