import pytest

from tennis_app.src.shared.dao import PlayerDAO
from tennis_app.src.shared.core import PersistentDatabaseDAO
from tennis_app.src.models import PlayerModel
from tennis_app.src.shared.dto import ReadPlayerDTO
from tennis_app.src.shared.exceptions import PlayerNotFoundError


@pytest.mark.slow
@pytest.mark.db
def test_insert():
    new_id: int = PlayerDAO.insert_one("a player")

    with PersistentDatabaseDAO.new_session() as session:
        player: PlayerModel = (
            session.query(PlayerModel).filter_by(name="a player").scalar()
        )
    assert player.id == new_id
    assert player.name == "a player"


@pytest.mark.slow
@pytest.mark.db
def test_select():
    res: ReadPlayerDTO = PlayerDAO.select_one_by_name("a player")
    assert res.name == "a player"

    res: ReadPlayerDTO = PlayerDAO.select_one_by_name("Bjorn Borg")
    assert res.name == "Bjorn Borg"
    assert res.p_id == 1

    with pytest.raises(PlayerNotFoundError):
        PlayerDAO.select_one_by_name("fake player")

    # test trying to add the same player second time doesn't change db data
    # and thus doesn't change the id
    PlayerDAO.insert_one("Bjorn Borg")
    res: ReadPlayerDTO = PlayerDAO.select_one_by_name("Bjorn Borg")
    assert res.p_id == 1
