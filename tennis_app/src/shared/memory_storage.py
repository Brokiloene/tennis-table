import threading
from typing import Dict
from uuid import UUID

from tennis_app.src.utils import get_uuid
from tennis_app.src.shared.tennis_game_logic import Match

class MemoryStorage:
    data: Dict[UUID, Match] = {}
    lock = threading.Lock()

    def create(player1_name: str, player2_name: str) -> UUID: 
        match_uuid = get_uuid()
        with MemoryStorage.lock:
            MemoryStorage.data[match_uuid] = Match(
                player1_name,
                player2_name
            )
        return match_uuid

    def read(match_uuid: UUID):
        """
        :raises: KeyError
        """
        with MemoryStorage.lock:
            return MemoryStorage.data[match_uuid]

    def update(match_uuid: UUID, player_num):
        """
        :raises: KeyError
        """
        with MemoryStorage.lock:
            MemoryStorage.data[match_uuid].add_game_point(player_num)

    def delete(match_uuid: UUID):
        """
        :raises: KeyError
        """
        with MemoryStorage.lock:
            MemoryStorage.data.pop(match_uuid)
