from app.repositories.pokemon_repo import PokemonRepository
from app.services.pokemon_service import PokemonService

POKEMON_REPOSITORY = PokemonRepository()
POKEMON_SERVICE = PokemonService(POKEMON_REPOSITORY)