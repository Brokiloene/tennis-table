import threading
import uuid
from uuid import UUID

import pytest

from tennis_app.src.shared.tennis_game_logic import Match
from tennis_app.src.shared.dao.match_memory_storage import MemoryStorageDAO, MatchNotFoundError


@pytest.fixture
def tennis_match_uuid() -> UUID:
    return MemoryStorageDAO.create("P1", "P2")


@pytest.mark.slow
def test_no_race_on_match_change_score(tennis_match_uuid: UUID):
    # a big number to check race condition
    NUMBER_OF_ADDITIONS = 100000

    def change_score_not_atomic(match_uuid: UUID):
        for _ in range(NUMBER_OF_ADDITIONS):
            # a non atomic operation
            int(1)
            # "P1" has id 1, "P2" has id 2
            MemoryStorageDAO.update(match_uuid, 1)
    
    t1 = threading.Thread(
        target=change_score_not_atomic, args=(tennis_match_uuid,)
    )
    t2 = threading.Thread(
        target=change_score_not_atomic, args=(tennis_match_uuid,)
    )
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    tennis_match: Match = MemoryStorageDAO.read(tennis_match_uuid)
    assert tennis_match.match_ended is True
    assert tennis_match.winner == "P1"
    assert tennis_match.points_added == NUMBER_OF_ADDITIONS*2


def test_crud(tennis_match_uuid: UUID):
    # read
    _: Match = MemoryStorageDAO.read(tennis_match_uuid)

    fake_uuid = uuid.uuid1()
    with pytest.raises(MatchNotFoundError):
        MemoryStorageDAO.read(fake_uuid)

    # update
    MemoryStorageDAO.update(tennis_match_uuid, 1)
    m = MemoryStorageDAO.read(tennis_match_uuid)
    assert m.points_added == 1

    with pytest.raises(MatchNotFoundError):
        MemoryStorageDAO.update(fake_uuid, 1)

    # delete
    with pytest.raises(MatchNotFoundError):
        MemoryStorageDAO.delete(fake_uuid)
    
    MemoryStorageDAO.delete(tennis_match_uuid)
    with pytest.raises(MatchNotFoundError):
        MemoryStorageDAO.read(tennis_match_uuid)
