import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tennis_app.src.shared.core import PersistentDatabaseDAO
from tennis_app.src.infrastructure.database import BaseModel
from tennis_app.src.models import PlayerModel, MatchModel
from tests.db.db_data import players, matches


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    test_engine = create_engine("sqlite:///:memory:", echo=False)
    PersistentDatabaseDAO.new_session = sessionmaker(
        test_engine, expire_on_commit=False
    )
    BaseModel.metadata.create_all(test_engine)

    with PersistentDatabaseDAO.new_session() as session:
        for name in players:
            session.add(PlayerModel(name=name))
        for tennis_match in matches:
            session.add(MatchModel(**tennis_match.asdict()))
        session.commit()

    yield

    BaseModel.metadata.drop_all(test_engine)
