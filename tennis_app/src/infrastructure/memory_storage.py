import threading
from typing import Dict, Any
from uuid import UUID


class MemoryStorage:
    data: Dict[UUID, Any] = {}
    lock = threading.Lock()
