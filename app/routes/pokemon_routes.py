import random

from flask import Blueprint, app, redirect, render_template, request, session, url_for
from app.repositories.pokemon_repo import PokemonRepository
from app.services.pokemon_service import PokemonService
from app.util.decorator_functions import login_requerido

pokemon_bp = Blueprint("pokemon", __name__)

repo = PokemonRepository()
service = PokemonService(repo)

@app.route('/', methods=["GET", "POST"])
@login_requerido
def listadoPokemon():
    trainer = session.get("trainer")
    error = None

    if request.method == "POST":
        nombre_pokemon = request.form.get("pokemon", "").strip().lower()
        pokemon_elegido = service.get_pokemons_by_type(nombre_pokemon)

        if not nombre_pokemon:
            error = "El nombre del pokemon es obligatorio."
        elif pokemon_elegido is None:
            error = "Pokemon no encontrado."
        else:
            rival = random.choice([p for p in POKEMONS if p["id"] != pokemon_elegido["id"]])
            total = len(pokemon_elegido["moves"])
            session["batalla"] = {
                "pokemon": pokemon_elegido["id"],
                "rival": rival["id"],
                "ataques": random.sample(range(total), min(4, total))
            }
            return redirect(url_for('battle'))

    tipo = request.args.get("tipo", "")
    media = request.args.get("media", "")

    tipos_pokemon = service.get_pokemon_types()
    pokemons_filtrados = []

    if tipo:
        pokemons_filtrados = service.get_pokemons_by_type(tipo)
    if media:
        pokemons_filtrados = service.get_pokemons_by_avg_range(media)

    return render_template('listado-pkm.html', pokemons=pokemons_filtrados,
                           trainer=trainer, tipos_pokemon=tipos_pokemon,
                           tipo=tipo, media=media, error=error)
        
@app.route('/<int:id>')
@login_requerido
def pokemon(id):
    pokemon = next((p for p in POKEMONS if p["id"] == id), None)

    if pokemon is None:
        return "Pokemon no encontrado", 404
    
    return render_template('pokemon.html', pokemon = pokemon)