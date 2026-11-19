from dataclasses import dataclass
from app.models.participant import Participant


@dataclass
class Battle():
    participants: list[Participant]
    winner: bool

    def atack(self, move_name):
        pass    

    def current_hp(self, participant):
        pass

    def is_over(self):
        return self.winner

    def log(self):
        pass