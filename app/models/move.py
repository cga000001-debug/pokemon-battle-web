from dataclasses import dataclass

@dataclass
class Move:
    name: str
    url: str
    accuracy: int
    power: int
    type: str