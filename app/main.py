import json, random, os
from flask import Flask, render_template, request, url_for, redirect, session
from pathlib import Path
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-solo-para-desarrollo")

RUTA_DATOS = Path(__file__).resolve().parent.parent / "data" / "pokemons-legendary.json"

with RUTA_DATOS.open(encoding="utf-8") as f:
    DATOS = json.load(f)
for pokemon in DATOS:
    pokemon["media"] = sum(stat["value"] for stat in pokemon["stats"]) / len(pokemon["stats"])

def login_requerido(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "trainer" not in session:
            return redirect(url_for("index"))
        return func(*args, **kwargs)
    return wrapper

@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')

    trainer = request.form.get("trainer","").strip()

    if not trainer:
        return render_template('index.html', error="El trainer es obligatorio.")
    if len(trainer) < 3 or len(trainer) > 15:
        return render_template('index.html', error="El trainer debe tener entre 3 y 15 caracteres.")

    session["trainer"] = trainer
    return redirect(url_for('listadoPokemon')) 

@app.route('/pokemons', methods=["GET", "POST"])
@login_requerido
def listadoPokemon():
    trainer = session.get("trainer")
    error = None

    if request.method == "POST":
        nombre_pokemon = request.form.get("pokemon", "").strip().lower()
        pokemon_elegido = next((p for p in DATOS if p["name"].lower() == nombre_pokemon), None)

        if not nombre_pokemon:
            error = "El nombre del pokemon es obligatorio."
        elif pokemon_elegido is None:
            error = "Pokemon no encontrado."
        else:
            rival = random.choice([p for p in DATOS if p["id"] != pokemon_elegido["id"]])
            total = len(pokemon_elegido["moves"])
            session["batalla"] = {
                "pokemon": pokemon_elegido["id"],
                "rival": rival["id"],
                "ataques": random.sample(range(total), min(4, total))
            }
            return redirect(url_for('battle'))

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
@login_requerido
def pokemon(id):
    pokemon = next((p for p in DATOS if p["id"] == id), None)

    if pokemon is None:
        return "Pokemon no encontrado", 404
    
    return render_template('pokemon.html', pokemon = pokemon)


@app.route('/battle')
@login_requerido
def battle():
    batalla = session.get("batalla")
    if not batalla:
        return redirect(url_for('listadoPokemon'))

    pokemon = next((p for p in DATOS if p["id"] == batalla["pokemon"]), None)
    pokemon_rival = next((p for p in DATOS if p["id"] == batalla["rival"]), None)
    
    if pokemon is None or pokemon_rival is None:
        session.pop("batalla", None)
        return redirect(url_for('listadoPokemon'))

    ataques = [pokemon["moves"][i] for i in batalla["ataques"]]

    listaRivales = [
        p for p in DATOS
        if p["id"] != pokemon["id"]
    ]

    return render_template('battle.html', pokemon=pokemon,
                           pokemon_rival=pokemon_rival, ataques=ataques)

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=8080)