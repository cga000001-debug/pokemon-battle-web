# Use asdict with dataclass
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    pokemon_name: str