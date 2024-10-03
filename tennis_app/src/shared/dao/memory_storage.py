from typing import Dict
from uuid import UUID

from tennis_app.src.shared.exceptions import MatchNotFoundError
from tennis_app.src.shared.memory_storage import MemoryStorage

class MemoryStorageDAO:
    def create(player1_name: str, player2_name: str) -> UUID:
        """
        :raises: MatchNotFoundError
        """   
        return MemoryStorage.create(player1_name, player2_name)
    
    def read(match_uuid: UUID):
        """
        :raises: MatchNotFoundError
        """
        try: 
            return MemoryStorage.read(match_uuid)
        except KeyError:
            raise MatchNotFoundError
    
    def update(match_uuid: UUID, player_num):
        """
        :raises: MatchNotFoundError
        """
        try: 
            return MemoryStorage.update(match_uuid, player_num)
        except KeyError:
            raise MatchNotFoundError
    
    def delete(match_uuid: UUID):
        """
        :raises: MatchNotFoundError
        """
        try:
            MemoryStorage.delete(match_uuid)
        except KeyError:
            raise MatchNotFoundError
