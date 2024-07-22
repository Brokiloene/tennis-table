from dataclasses import dataclass

from .base import BaseDTO

@dataclass
class ReadMatchDTO(BaseDTO):
    player1_name: str
    player2_name: str
    winner_name: str
    score: str

@dataclass
class CreateMatchDTO(BaseDTO):
    uuid: str
    player1_id: int
    player2_id: int
    winner_id: int
    score: str

