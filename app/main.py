import json, random
from flask import Flask, render_template, request
from pathlib import Path

app = Flask(__name__)

RUTA_DATOS = Path(__file__).resolve().parent.parent / "data" / "pokemons-legendary.json"

with RUTA_DATOS.open(encoding="utf-8") as f:
    DATOS = json.load(f)
for pokemon in DATOS:
    pokemon["media"] = sum(stat["value"] for stat in pokemon["stats"]) / len(pokemon["stats"])

@app.route('/')
def index():
    return render_template('index.html')
        
@app.route('/pokemons', methods=["GET","POST"])
def listadoPokemon():
    if request.method == "POST":
        trainer = request.form.get("trainer","").strip()
    else:
        trainer = request.args.get("trainer","").strip()

    tipo = request.args.get("tipo","")
    media = request.args.get("media", "")
    
    tipos_pokemon = sorted(set(t for pokemon in DATOS for t in pokemon["types"]))

    pokemons_filtrados = DATOS

    if tipo:
        pokemons_filtrados = [
            pokemon for pokemon in pokemons_filtrados
            if tipo in pokemon["types"]
        ]

    if media:
        if media == "baja":
            pokemons_filtrados = [
                pokemon for pokemon in pokemons_filtrados
                if pokemon["media"] < 100
            ]
        elif media == "media":
            pokemons_filtrados = [
                pokemon for pokemon in pokemons_filtrados
                if pokemon["media"] < 112
            ]
        elif media == "alta":
            pokemons_filtrados = [
                pokemon for pokemon in pokemons_filtrados
                if pokemon["media"] > 112
            ]

    return render_template('listado-pkm.html', pokemons=pokemons_filtrados, trainer=trainer, tipos_pokemon=tipos_pokemon, tipo=tipo, media=media)
        

@app.route('/pokemons/<int:id>')
def pokemon(id):

    pokemon = next((p for p in DATOS if p["id"] == id), None)

    if pokemon is None:
        return "Pokemon no encontrado", 404
    
    return render_template('pokemon.html', pokemon = pokemon)

@app.route('/battle', methods=["GET", "POST"])
def battle():
    if request.method == "GET":
        return render_template('battle.html')

    nombre_pokemon = request.form["pokemon"].strip().lower()
    trainer = request.form.get("trainer", "").strip()
    error = None

    pokemon = next((p for p in DATOS if p["name"] == nombre_pokemon), None)

    if not nombre_pokemon:
        error = "El nombre del pokemon es obligatorio"
        return render_template('battle.html')
    
    if pokemon is None:
        error = "Pokemon no encontrado"
        return render_template('battle.html')

    ataques = random.sample(pokemon["moves"], 4);

    listaRivales = [
        p for p in DATOS
        if p["id"] != pokemon
    ]

    pokemon_rival = random.choice(listaRivales);


    return render_template('battle.html')

if __name__ == '__main__':
    app.run(port=8080)