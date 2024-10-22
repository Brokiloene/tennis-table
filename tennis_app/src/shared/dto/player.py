from dataclasses import dataclass

from tennis_app.src.shared.core import BaseDTO


@dataclass
class ReadPlayerDTO(BaseDTO):
    p_id: int
    name: str
