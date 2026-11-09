import random

from flask import Blueprint, app, redirect, render_template, request, session, url_for
from app.repositories.pokemon_repo import PokemonRepository
from app.services.pokemon_service import PokemonService
from app.util.decorator_functions import login_requerido

pokemon_bp = Blueprint("pokemon", __name__)
service = PokemonService(PokemonRepository())

@pokemon_bp.route('/', methods=["GET", "POST"])
@login_requerido
def listadoPokemon():
    trainer = session.get("trainer")
    error = None

    if request.method == "POST":
        nombre_pokemon = request.form.get("pokemon", "").strip().lower()
        elegido = service.get_pokemon_by_name(nombre_pokemon)

        if not nombre_pokemon:
            error = "El nombre del pokemon es obligatorio."
        elif elegido is None:
            error = "Pokemon no encontrado."
        else:
            rival = random.choice([p for p in service.get_all_pokemon() if p.id != elegido.id])
            total = len(elegido.moves)
            session["batalla"] = {
                "pokemon": elegido.id,
                "rival": rival.id,
                "ataques": random.sample(range(total), min(4, total))
            }
            return redirect(url_for('battle.battle'))

    tipo = request.args.get("tipo", "")
    media = request.args.get("media", "")

    return render_template('listado-pkm.html', pokemons=service.filter_pokemons(tipo, media),
                           trainer=trainer, tipos_pokemon=service.get_pokemon_types(),
                           tipo=tipo, media=media, error=error)
        
@pokemon_bp.route('/<int:id>')
@login_requerido
def pokemon(id):
    pokemon = service.get_pokemon_by_id(id)
    if pokemon is None:
        return "Pokemon no encontrado", 404
    return render_template('pokemon.html', pokemon = pokemon)