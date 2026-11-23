from dataclasses import dataclass
from app.models.participant import Participant
from app.models.turn import Turn


@dataclass
class Battle():
    participants: list[Participant]
    turns: list[Turn]
    winner: bool

    def attack(self, move_name):
        pass
      
    def current_hp(self, participant):
        return self.participants[participant].pokemon.max

    def is_over(self):
        return self.winner

    def log(self):
        pass