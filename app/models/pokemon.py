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
        if not self.stats:
            return 0

        return sum(s["value"] for s in self.stats) / len(self.stats)