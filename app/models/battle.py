from dataclasses import asdict, dataclass
from app.models.participant import Participant
from app.models.turn import Turn


@dataclass
class Battle():
    participants: list[Participant]
    turns: list[Turn]
    winner: bool

    def attack(self, move_name):
        attacker = 0
        if self.turns:
            attacker = not self.turns[-1].attacker

        if self.winner:
            # Exception
            return
        if move_name not in [m["name"] for m in self.participants[not attacker].pokemon.moves]:
            # Excepcion
            return        

        

      
    def current_hp(self, participant):
        for t in reversed(self.turns):
            if (t.attacker != self.participants):
                return t.remaining_hp
        return self.participants[participant].max_hp
    
    def is_over(self):
        return self.winner is not None

    def log(self):
        pass

    def to_dict(self):
        return {
            "participants": [ p.to_dict for p in self.participants],
            "turns": [asdict(t) for t in self.turns],
            "winner": self.winner
        }