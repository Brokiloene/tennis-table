from dataclasses import dataclass

from .base import BaseDTO

@dataclass
class ReadPlayerDTO(BaseDTO):
    p_id: int
    name: str
