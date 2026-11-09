from flask import Blueprint, app, redirect, render_template, session, url_for

from app.util.decorator_functions import login_requerido
from app.repositories.pokemon_repo import PokemonRepository
from app.services.pokemon_service import PokemonService

battle_bp = Blueprint("battle", __name__)
service = PokemonService(PokemonRepository())

@battle_bp.route('/')
@login_requerido
def battle():
    batalla = session.get("batalla")
    if not batalla:
        return redirect(url_for('pokemon.listadoPokemon'))

    pokemon = service.get_pokemon_by_id(batalla["pokemon"])
    pokemon_rival = service.get_pokemon_by_id(batalla["rival"])
    
    if pokemon is None or pokemon_rival is None:
        session.pop("batalla", None)
        return redirect(url_for('pokemon.listadoPokemon'))

    ataques = [pokemon.moves[i] for i in batalla["ataques"]]

    return render_template('battle.html', pokemon=pokemon,
                           pokemon_rival=pokemon_rival, ataques=ataques)