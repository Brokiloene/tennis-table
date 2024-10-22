from dataclasses import dataclass

from tennis_app.src.shared.core import BaseDTO

@dataclass
class ReadMatchDTO(BaseDTO):
    player1_name: str
    player2_name: str
    score: str

@dataclass
class CreateMatchDTO(BaseDTO):
    uuid: str
    player1_id: int
    player2_id: int
    winner_id: int
    score: str

@dataclass  
class ViewMatchDTO(BaseDTO):
    p1_name: str
    p2_name: str

    p1_s1: str
    p1_s2: str
    p1_s3: str

    p2_s1: str
    p2_s2: str
    p2_s3: str
