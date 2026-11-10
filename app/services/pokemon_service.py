from app.repositories.pokemon_repo import PokemonRepository

class PokemonService:
    def __init__(self, repo: PokemonRepository):
        self.repo = repo

    def get_all_pokemon(self):
        return self.repo.get_all_pokemon()

    def get_pokemon_by_id(self, pokemon_id):
        return self.repo.get_pokemon_by_id(pokemon_id)

    def get_pokemon_by_name(self, pokemon_name):
        return self.repo.get_pokemon_by_name(pokemon_name)

    def get_pokemon_types(self):
        return self.repo.get_pokemon_types()

    def filter_pokemons(self, tipo="", media=""):
        pokemons = self.repo.get_all_pokemon()
        if tipo:
            pokemons = [p for p in pokemons if tipo in p.types]
        if media:
            ids = {p.id for p in self.repo.get_pokemons_by_avg_range(media)}
            pokemons = [p for p in pokemons if p.id in ids]
        return pokemons