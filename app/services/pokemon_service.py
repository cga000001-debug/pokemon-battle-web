from app.repositories.pokemon_repo import PokemonRepository

class PokemonService:
    def __init__(self, repo: PokemonRepository):
        self.repo = repo

    def get_all_pokemons(self):
        return self.repo.get_all_pokemons()

    def get_pokemon_by_id(self, pokemon_id):
        return self.repo.get_pokemon_by_id(pokemon_id)

    def get_pokemon_by_name(self, pokemon_name):
        return next((p for p in self.get_all_pokemons() if p.name.lower() == pokemon_name.lower()), None)

    def get_pokemon_types(self):
        return sorted({tipo for p in self.get_all_pokemons() for tipo in p.types})

    def get_pokemons_by_avg_range(self, range):
        if range == "baja":
            return [p for p in self.get_all_pokemons() if p.get_avg() < 100]
        elif range == "media":
            return [p for p in self.get_all_pokemons() if 100 <= p.get_avg() <= 112]
        elif range == "alta":
            return [p for p in self.get_all_pokemons() if p.get_avg() > 112]
        return []

    def filter_pokemons(self, tipo="", media=""):
        pokemons = self.get_all_pokemons()
        if tipo:
            pokemons = [p for p in pokemons if tipo in [t for t in p.types]]
        if media: 
            ranges = {
                "baja": lambda p: p.get_avg() < 100,
                "media": lambda p: 100 <= p.get_avg() <= 112,
                "alta": lambda p: p.get_avg() > 112
            }
            if media in ranges:
                pokemons = [p for p in pokemons if ranges[media](p)]
        return pokemons
    