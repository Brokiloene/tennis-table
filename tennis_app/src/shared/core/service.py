from abc import abstractmethod

class BaseService:
    @abstractmethod
    def execute(self):
        pass
