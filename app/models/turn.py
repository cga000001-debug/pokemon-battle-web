from dataclasses import dataclass

from app.models.move import Move

@dataclass
class Turn:
    number: int
    attacker: int
    move: Move
    hit: bool
    damage: int
    remaining_hp: int
