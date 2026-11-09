from dataclasses import dataclass

@dataclass
class Pokemon:
    id: int
    height: int
    name: str
    stats: list
    sprites: dict
    types: list
    weight: int
    moves: list
    media: float = 0.0