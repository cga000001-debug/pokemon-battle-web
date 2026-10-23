import json, random
from flask import Flask, render_template, request, url_for, redirect
from pathlib import Path

app = Flask(__name__)

RUTA_DATOS = Path(__file__).resolve().parent.parent / "data" / "pokemons-legendary.json"

with RUTA_DATOS.open(encoding="utf-8") as f:
    DATOS = json.load(f)
for pokemon in DATOS:
    pokemon["media"] = sum(stat["value"] for stat in pokemon["stats"]) / len(pokemon["stats"])


@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        trainer = request.form.get("trainer","").strip()

        if not trainer:
            return render_template('index.html', error="El trainer es obligatorio.")
        if len(trainer) < 3 or len(trainer) > 15:
            return render_template('index.html', error="El trainer debe tener entre 3 y 15 caracteres.")

    return redirect(url_for('listadoPokemon', trainer=trainer)) 

@app.route('/pokemons', methods=["GET", "POST"])
def listadoPokemon():
    trainer = request.args.get('trainer', '').strip()

    if not trainer:
        return redirect(url_for('index'))

    error = None

    if request.method == "POST":
        nombre_pokemon = request.form.get("pokemon", "").strip().lower()
        pokemon_elegido = next((p for p in DATOS if p["name"].lower() == nombre_pokemon), None)

        if not nombre_pokemon:
            error = "El nombre del pokemon es obligatorio."
        elif pokemon_elegido is None:
            error = "Pokemon no encontrado."
        else:
            return redirect(url_for('battle', trainer=trainer, pokemon=pokemon_elegido["name"]))

    tipo = request.args.get("tipo", "")
    media = request.args.get("media", "")

    tipos_pokemon = sorted({tipo for pokemon in DATOS for tipo in pokemon["types"]})
    pokemons_filtrados = DATOS

    if tipo:
        pokemons_filtrados = [pokemon for pokemon in pokemons_filtrados if tipo in pokemon["types"]]

    if media == "baja":
        pokemons_filtrados = [pokemon for pokemon in pokemons_filtrados if pokemon["media"] < 100]
    elif media == "media":
        pokemons_filtrados = [pokemon for pokemon in pokemons_filtrados if 100 <= pokemon["media"] <= 112]
    elif media == "alta":
        pokemons_filtrados = [pokemon for pokemon in pokemons_filtrados if pokemon["media"] > 112]

    return render_template('listado-pkm.html', pokemons=pokemons_filtrados,
                           trainer=trainer, tipos_pokemon=tipos_pokemon,
                           tipo=tipo, media=media, error=error)
        
@app.route('/pokemon/<int:id>')
def pokemon(id):

    pokemon = next((p for p in DATOS if p["id"] == id), None)

    if pokemon is None:
        return "Pokemon no encontrado", 404
    
    return render_template('pokemon.html', pokemon = pokemon)


@app.route('/battle')
def battle():
    nombre_pokemon = request.args.get("pokemon", "").strip().lower()
    trainer = request.form.get("trainer", "").strip()

    if not trainer:
        return redirect(url_for('index'))

    pokemon = next((p for p in DATOS if p["name"] == nombre_pokemon), None)
    
    if pokemon is None:
        return redirect(url_for('listadoPokemon', trainer=trainer))

    ataques = random.sample(pokemon["moves"], min(4, len(pokemon["moves"])))

    listaRivales = [
        p for p in DATOS
        if p["id"] != pokemon["id"]
    ]

    pokemon_rival = random.choice(listaRivales)

    return render_template('battle.html', pokemon=pokemon,
                           pokemon_rival=pokemon_rival, ataques=ataques,
                           trainer=trainer)

if __name__ == '__main__':
    app.run(port=8080)