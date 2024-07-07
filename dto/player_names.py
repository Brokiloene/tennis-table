from dataclasses import dataclass

from .base import BaseDto

@dataclass
class PlayerNamesDTO(BaseDto):
    name_p1: str
    name_p2: str


