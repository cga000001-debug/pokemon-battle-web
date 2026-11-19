from dataclasses import dataclass

from app.models.pokemon import Pokemon


@dataclass
class Participant:
    trainer: str
    pokemon: Pokemon