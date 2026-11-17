from app.repositories.pokemon_repo import PokemonRepository

class PokemonService:
    def __init__(self, repo: PokemonRepository):
        self.repo = repo

    def get_all_pokemon(self):
        return self.repo.get_all_pokemon()

    def get_pokemon_by_id(self, pokemon_id):
        return self.repo.get_pokemon_by_id(pokemon_id)

    def get_pokemon_by_name(self, pokemon_name):
        return next((p for p in self.get_all_pokemon if p.name.lower() == pokemon_name.lower()), None)

    def get_pokemon_types(self, pokemon_type):
        return sorted({tipo for p in self.get_all_pokemon for tipo in p.types})

    def get_pokemons_by_avg_range(self, range):
        if range == "baja":
            return [p for p in self.get_all_pokemon if p.get_avg() < 100]
        elif range == "media":
            return [p for p in self.get_all_pokemon if 100 <= p.get_avg() <= 112]
        elif range == "alta":
            return [p for p in self.get_all_pokemon if p.get_avg() > 112]
        return []

    def filter_pokemons(self, tipo="", media=""):
        pokemons = self.repo.get_all_pokemon()
        if tipo:
            pokemons = [p for p in pokemons if tipo in p.types]
        if media:  # Mirar esto
            ids = {p.id for p in self.repo.get_pokemons_by_avg_range(media)}
            pokemons = [p for p in pokemons if p.id in ids]
        return pokemons
    