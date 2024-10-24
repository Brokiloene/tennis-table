from abc import abstractmethod

from tennis_app.src.models import session_factory


class PersistentDatabaseDAO:
    new_session = session_factory

    @staticmethod
    @abstractmethod
    def insert_one(*args, **kwargs):
        pass
