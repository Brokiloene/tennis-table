from uuid import UUID

from tennis_app.src.utils import get_uuid
from tennis_app.src.shared.exceptions import MatchNotFoundError
from tennis_app.src.infrastructure.memory_storage import MemoryStorage
from tennis_app.src.shared.tennis_game_logic import Match


class MemoryStorageDAO:
    def create(player1_name: str, player2_name: str) -> UUID:
        key = get_uuid()
        with MemoryStorage.lock:
            MemoryStorage.data[key] = Match(player1_name, player2_name)
        return key

    def read(match_uuid: UUID):
        """
        :raises: MatchNotFoundError
        """
        try:
            with MemoryStorage.lock:
                res = MemoryStorage.data[match_uuid]
            return res
        except KeyError:
            raise MatchNotFoundError

    def update(match_uuid: UUID, player_num: int):
        """
        :raises: MatchNotFoundError
        """
        try:
            with MemoryStorage.lock:
                MemoryStorage.data[match_uuid].add_game_point(player_num)
        except KeyError:
            raise MatchNotFoundError

    def delete(match_uuid: UUID):
        """
        :raises: MatchNotFoundError
        """
        try:
            MemoryStorage.data.pop(match_uuid)
        except KeyError:
            raise MatchNotFoundError
