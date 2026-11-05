import json
from pathlib import Path
from app.models.pokemon import Pokemon

RUTA_DATOS = Path(__file__).resolve().parent.parent / "data" / "pokemons-legendary.json"

def load_data():
    with RUTA_DATOS.open(encoding="utf-8") as f:
        DATOS = json.load(f)
    for pokemon in DATOS:
        pokemon["media"] = sum(stat["value"] for stat in pokemon["stats"]) / len(pokemon["stats"])
    return DATOS
    

def get_all_pokemon():
    pokemons = []
    pokemons_fichero = load_data()
    for p in pokemons_fichero:
        pokemons.append(Pokemon(**p))
    

    return pokemons

def get_pokemon_by_id(pokemon_id):
    for p in get_all_pokemon():
        if p["id"] == pokemon_id:
            return p
    return None

def get_pokemon_by_name(pokemon_name):
    for p in get_all_pokemon():
        if p["name"] == pokemon_name:
            return p
    return None

def get_pokemons_by_type(pokemon_type):
    pokemons_by_type = []
    for p in get_all_pokemon():
        if p["type"] == pokemon_type:
            pokemons_by_type.append(p)

    return pokemons_by_type
    