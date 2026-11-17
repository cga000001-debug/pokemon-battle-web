from dataclasses import dataclass

from app.models.move import Move

@dataclass
class Pokemon:
    id: int
    height: int
    name: str
    stats: list
    sprites: dict
    types: list
    weight: int
    moves: list[Move]

    def get_avg(self):
        sum(self.stats["value"] for s in self.stats) / len(self.stats)