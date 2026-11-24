from dataclasses import dataclass

from app.models.pokemon import Pokemon


@dataclass
class Participant:
    trainer: str
    pokemon: Pokemon

    @property
    def max_hp(self):
        return self.pokemon.stats["hp"]

    def to_dict(self):
        return {
            "trainer": self.trainer,
            "pokemon": {
                "id": self.pokemon.id, "name": self.pokemon.name, "types": self.pokemon.types,
                "stats": self.pokemon.stats,
                "moves": self.pokemon.moves,
                "max_hp": self.max_hp
            }
        }