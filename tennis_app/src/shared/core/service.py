from abc import abstractmethod


class BaseService:
    @staticmethod
    @abstractmethod
    def execute(*args, **kwargs):
        pass
