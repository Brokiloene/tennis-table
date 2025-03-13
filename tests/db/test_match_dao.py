import math

import pytest

from tennis_app.src.shared.dao import MatchDAO, PlayerDAO
from tennis_app.src.shared.dto import CreateMatchDTO, ReadMatchDTO
from tennis_app.src.shared.core import PersistentDatabaseDAO
from tennis_app.src.models import MatchModel


@pytest.mark.slow
@pytest.mark.db
def test_insert():
    # in db there are no checks for correctness of the match result
    new_match = CreateMatchDTO("a new uuid", 1, 2, 1, "6 0 6 0 0 0")
    MatchDAO.insert_one(new_match)
    with PersistentDatabaseDAO.new_session() as session:
        res: MatchModel = (
            session.query(MatchModel).filter_by(uuid="a new uuid").scalar()
        )

    assert res.uuid == new_match.uuid
    assert res.player1_id == new_match.player1_id
    assert res.player2_id == new_match.player2_id
    assert res.winner_id == new_match.winner_id
    assert res.score == new_match.score

    # adding the same match second time change nothing
    MatchDAO.insert_one(new_match)
    with PersistentDatabaseDAO.new_session() as session:
        res2: MatchModel = (
            session.query(MatchModel).filter_by(uuid="a new uuid").scalar()
        )
    # id of match doesn't change
    assert res.id == res2.id


@pytest.mark.slow
@pytest.mark.db
def test_get_cnt_of_matches_empty():
    new_id: int = PlayerDAO.insert_one("player for get_cnt_of_matches_empty")
    # no matches with this player yet
    res = MatchDAO.get_cnt_of_matches(search_name="player for get_cnt_of_matches_empty")
    assert res == 0


@pytest.mark.slow
@pytest.mark.db
def test_get_cnt_of_matches_add_one():
    new_id: int = PlayerDAO.insert_one("player for get_cnt_of_matches_add_one")

    # add the match
    # id 1 is Bjorn Borg
    bjorn_borg_matches_cnt_pre = MatchDAO.get_cnt_of_matches(search_name="Bjorn Borg")

    new_match = CreateMatchDTO("a new uuid for cnt", 1, new_id, 1, "6 0 6 0 0 0")
    MatchDAO.insert_one(new_match)
    res = MatchDAO.get_cnt_of_matches(
        search_name="player for get_cnt_of_matches_add_one"
    )
    assert res == 1

    bjorn_borg_matches_cnt_aft = MatchDAO.get_cnt_of_matches(search_name="Bjorn Borg")
    assert bjorn_borg_matches_cnt_pre + 1 == bjorn_borg_matches_cnt_aft


@pytest.mark.slow
@pytest.mark.db
def test_get_cnt_of_matches_by_partial_name():
    # check partial coincidence
    new_id2: int = PlayerDAO.insert_one(
        "player for get_cnt_of_matches_by_partial_name 2"
    )
    new_match = CreateMatchDTO("a new uuid for cnt2", 1, new_id2, 1, "6 0 6 0 0 0")
    MatchDAO.insert_one(new_match)
    res = MatchDAO.get_cnt_of_matches(
        search_name="player for get_cnt_of_matches_by_partial_name"
    )
    assert res == 1


@pytest.mark.slow
@pytest.mark.db
def test_get_cnt_of_matches_by_fake_name():
    res = MatchDAO.get_cnt_of_matches(search_name="a fake non-existing player")
    assert res == 0


@pytest.mark.slow
@pytest.mark.db
def test_fetch_all():
    cnt_of_all_matches = MatchDAO.get_cnt_of_matches(search_name=None)
    res = MatchDAO.fetch_all(page=1, matches_on_page_cnt=cnt_of_all_matches)
    # all present matches should be selected
    assert len(res) == cnt_of_all_matches

    res = MatchDAO.fetch_all(page=1, matches_on_page_cnt=1)
    assert len(res) == 1

    res = MatchDAO.fetch_all(page=1, matches_on_page_cnt=0)
    assert len(res) == 0

    new_id: int = PlayerDAO.insert_one("player for fetch_all")
    # id 1 is Bjorn Borg
    new_match = CreateMatchDTO("a new uuid for fetch all", 1, new_id, 1, "6 0 6 0 0 0")
    MatchDAO.insert_one(new_match)

    cnt_of_all_matches = MatchDAO.get_cnt_of_matches(search_name=None)
    res = MatchDAO.fetch_all(page=1, matches_on_page_cnt=cnt_of_all_matches)
    # newly added match should be at the end of the list
    check_match = ReadMatchDTO("Bjorn Borg", "player for fetch_all", "6 0 6 0 0 0")
    assert res[-1] == check_match


@pytest.mark.slow
@pytest.mark.db
def test_page_offset_logic():
    def check_last_page_odd():
        res = MatchDAO.fetch_all(page=last_page, matches_on_page_cnt=2)
        assert len(res) == 1

    def check_last_page_even():
        res = MatchDAO.fetch_all(page=last_page, matches_on_page_cnt=2)
        assert len(res) == 2

    cnt_of_all_matches = MatchDAO.get_cnt_of_matches(search_name=None)

    # check offset logic
    new_match = CreateMatchDTO("a new uuid for page offset", 1, 1, 1, "6 0 6 0 0 0")
    last_page = math.ceil(cnt_of_all_matches / 2)
    if cnt_of_all_matches % 2 == 1:
        # if cnt_of_all_matches is odd then on the last page (with 2 mathes on each)
        # should be only one match
        check_last_page_odd()
        MatchDAO.insert_one(new_match)
    else:
        # otherwise there should be 2 matches on the last page
        check_last_page_even()
        MatchDAO.insert_one(new_match)

    # repeat to check both possibilities
    cnt_of_all_matches = MatchDAO.get_cnt_of_matches(search_name=None)
    last_page = math.ceil(cnt_of_all_matches / 2)

    if cnt_of_all_matches % 2 == 1:
        check_last_page_odd()
    else:
        check_last_page_even()


@pytest.mark.slow
@pytest.mark.db
def test_fetch_filtered_empty():
    new_id: int = PlayerDAO.insert_one("player for fetch_filtered_empty")

    # no matches with this player yet
    res = MatchDAO.fetch_filtered(
        search_query="player for fetch_fetch_filtered_emptyfiltered",
        page=1,
        matches_on_page_cnt=2,
    )
    assert len(res) == 0


@pytest.mark.slow
@pytest.mark.db
def test_fetch_filtered():
    new_id: int = PlayerDAO.insert_one("player for fetch_filtered")

    new_match = CreateMatchDTO(
        "a new uuid for fetch filtered", 1, new_id, 1, "6 0 6 0 0 0"
    )
    MatchDAO.insert_one(new_match)

    # one match must be found
    res = MatchDAO.fetch_filtered(
        search_query="player for fetch_filtered", page=1, matches_on_page_cnt=2
    )
    assert len(res) == 1

    # only one match exists, so the second page must be empty
    res = MatchDAO.fetch_filtered(
        search_query="player for fetch_filtered", page=2, matches_on_page_cnt=2
    )
    print("=============", res)
    assert len(res) == 0
