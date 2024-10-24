from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class BaseDTO:
    def asdict(self) -> dict[str, Any]:
        return asdict(self)
