import threading
from uuid import UUID

from tennis_app.src.utils import get_uuid
from tennis_app.src.shared.exceptions import MatchNotFoundError
from tennis_app.src.infrastructure.memory_storage import MemoryStorage
from tennis_app.src.shared.tennis_game_logic import Match


class MemoryStorageDAO:
    _storage = MemoryStorage()
    _lock = threading.Lock()

    @staticmethod
    def create(player1_name: str, player2_name: str) -> UUID:
        key = get_uuid()
        MemoryStorageDAO._storage.put(key, Match(player1_name, player2_name))

        # MemoryStorage.data[key] = Match(player1_name, player2_name)
        return key

    @staticmethod
    def read(match_uuid: UUID) -> Match:
        """
        :raises: MatchNotFoundError
        """
        try:
            with MemoryStorageDAO._lock:
                res = MemoryStorageDAO._storage.get_value(match_uuid)
                # res = MemoryStorage.data[match_uuid]
                return res
        except KeyError:
            raise MatchNotFoundError

    @staticmethod
    def update(match_uuid: UUID, player_num: int) -> None:
        """
        :raises: MatchNotFoundError
        """
        try:
            with MemoryStorageDAO._lock:
                res: Match = MemoryStorageDAO._storage.get_value(match_uuid)
                res.add_game_point(player_num)
                MemoryStorageDAO._storage.update_value(match_uuid, res)
        except KeyError:
            raise MatchNotFoundError

    @staticmethod
    def delete(match_uuid: UUID) -> None:
        """
        :raises: MatchNotFoundError
        """
        try:
            with MemoryStorageDAO._lock:
                MemoryStorageDAO._storage.delete(match_uuid)
        except KeyError:
            raise MatchNotFoundError
