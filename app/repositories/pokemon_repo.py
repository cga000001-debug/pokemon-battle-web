import json
from dataclasses import fields
from pathlib import Path
from app.models.pokemon import Pokemon

CAMPOS = {f.name for f in fields(Pokemon)}

class PokemonRepository:

    def __init__(self, ruta=None):
        self.ruta = ruta or Path(__file__).resolve().parent.parent.parent / "data" / "pokemons-legendary.json"
        self._pokemons = self._load_data()


    def _load_data(self):
        with open(self.ruta, encoding="utf-8") as f:
            datos = json.load(f)
        pokemons = []
        for d in datos:
            p = Pokemon(**{k: v for k, v in d.items() if k in CAMPOS})
            p.media = sum(s["value"] for s in p.stats) / len(p.stats)
            pokemons.append(p)
        return pokemons
    

    def get_all_pokemon(self):
        return list(self._pokemons)
    
    def get_pokemon_by_id(self, pokemon_id):
        return next((p for p in self._pokemons if p.id == pokemon_id), None)

    def get_pokemon_by_name(self, pokemon_name):
        return next((p for p in self._pokemons if p.name.lower() == pokemon_name.lower()), None)

    def get_pokemons_by_type(self, pokemon_type):
        return next((p for p in self._pokemons if pokemon_type in p.types), None)

    def get_pokemons_by_avg_range(self, range):
        if range == "baja":
                return [p for p in self._pokemons if p.media < 100]
        elif range == "media":
                return [p for p in self._pokemons if 100 <= p.media <= 112]
        elif range == "alta":
                return [p for p in self._pokemons if p.media > 112]
        return []

    def get_pokemon_types(self):
        return sorted({tipo for p in self._pokemons for tipo in p.types})
