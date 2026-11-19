import json
from dataclasses import fields
from pathlib import Path
from app.models.pokemon import Pokemon

CAMPOS = {f.name for f in fields(Pokemon)}

class PokemonRepository:

    def __init__(self, ruta=None):
        self.ruta = ruta or Path(__file__).resolve().parents[2]/ "data" / "pokemons-legendary.json"
        self._pokemons = self._load_data()

    def _load_data(self):
        with open(self.ruta, encoding="utf-8") as f:
            datos = json.load(f)
        return [
            Pokemon(**{k: v for k, v in d.items() if k in CAMPOS})
            for d in datos
        ]

    def get_all_pokemons(self):
        return self._pokemons.copy()
    
    def get_pokemon_by_id(self, pokemon_id):
        return next((p for p in self._pokemons if p.id == pokemon_id), None)