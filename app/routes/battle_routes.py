from flask import Blueprint, app, redirect, render_template, session, url_for

from app.util.decorator_functions import login_requerido
from app.repositories.pokemon_repo import load_data

battle_bp = Blueprint("battle", __name__)
POKEMONS = load_data()

@app.route('/')
@login_requerido
def battle():
    batalla = session.get("batalla")
    if not batalla:
        return redirect(url_for('listadoPokemon'))

    pokemon = next((p for p in POKEMONS if p["id"] == batalla["pokemon"]), None)
    pokemon_rival = next((p for p in POKEMONS if p["id"] == batalla["rival"]), None)
    
    if pokemon is None or pokemon_rival is None:
        session.pop("batalla", None)
        return redirect(url_for('listadoPokemon'))

    ataques = [pokemon["moves"][i] for i in batalla["ataques"]]

    return render_template('battle.html', pokemon=pokemon,
                           pokemon_rival=pokemon_rival, ataques=ataques)