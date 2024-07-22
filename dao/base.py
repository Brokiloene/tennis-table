from models import session_factory

class BaseDAO:
    new_session = session_factory
    def __init__(self) -> None:
        self.session_factory = session_factory
