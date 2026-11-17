from flask import Blueprint, app, redirect, render_template, session, url_for

from app.util.decorator_functions import login_requerido
from app.deps import POKEMON_SERVICE

battle_bp = Blueprint("battle", __name__)

@battle_bp.route('/')
@login_requerido
def battle():
    batalla = session.get("batalla")
    if not batalla:
        return redirect(url_for('pokemon.listadoPokemon'))

    pokemon = POKEMON_SERVICE.get_pokemon_by_id(batalla["pokemon"])
    pokemon_rival = POKEMON_SERVICE.get_pokemon_by_id(batalla["rival"])
    
    if pokemon is None or pokemon_rival is None:
        session.pop("batalla", None)
        return redirect(url_for('pokemon.listadoPokemon'))

    ataques = [pokemon.moves[i] for i in batalla["ataques"]]

    return render_template('battle.html', pokemon=pokemon,
                           pokemon_rival=pokemon_rival, ataques=ataques)