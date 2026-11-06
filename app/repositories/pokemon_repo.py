import json
from pathlib import Path
from app.models.pokemon import Pokemon

class PokemonRepository:

    def __init__(self, ruta=None):
        self.ruta = ruta or Path(__file__).resolve().parent.parent / "data" / "pokemons-legendary.json"


    def load_data(self):
        DATOS = []
        with open(self.ruta, encoding="utf-8") as f:
            DATOS = json.load(f)
        for pokemon in DATOS:
            pokemon["media"] = sum(stat["value"] for stat in pokemon["stats"]) / len(pokemon["stats"])
        return DATOS
    

    def get_all_pokemon(self):
        pokemons = []
        for p in self.load_data():
            pokemons.append(Pokemon(**p))
        return pokemons

    def get_pokemon_by_id(self, pokemon_id):
        for p in self.load_data():
            if p["id"] == pokemon_id:
                return p
        return None

    def get_pokemon_by_name(self, pokemon_name):
        for p in self.load_data():
            if p["name"] == pokemon_name:
                return p
        return None

    def get_pokemons_by_type(self, pokemon_type):
        pokemons_by_type = []
        for p in self.load_data(): 
            if p["type"] == pokemon_type:
                pokemons_by_type.append(p)
        return pokemons_by_type

    def get_pokemons_by_avg_range(self, pokemon_avg):
        pokemons_by_avg_range = []
        if pokemon_avg == "baja":
                for p in self.load_data(): 
                    if p["media"] < 100:
                        pokemons_by_avg_range.append(p)
        elif pokemon_avg == "media":
                for p in self.load_data(): 
                    if 100 <= p["media"] <= 112:
                        pokemons_by_avg_range.append(p)
        elif pokemon_avg == "alta":
                for p in self.load_data(): 
                    if p["media"] > 112:
                        pokemons_by_avg_range.append(p)

        return pokemons_by_avg_range

    def get_pokemon_types(self):
        pokemon_types = sorted({tipo for pokemon in self.load_data() for tipo in pokemon["types"]})
        return pokemon_types