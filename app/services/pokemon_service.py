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
    
    def get_pokemons_by_type(self, pokemon_type):
        return self.repo.get_pokemons_by_type(pokemon_type)

    def get_pokemons_by_avg_range(self, pokemon_avg):
        return self.repo.get_pokemons_by_avg_range(pokemon_avg)

    def get_pokemon_types(self):
        return self.repo.get_pokemon_types()