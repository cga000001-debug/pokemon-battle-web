import json
from flask import Flask, render_template, request
from pathlib import Path

app = Flask(__name__)

RUTA_DATOS = Path(__file__).resolve().parent.parent / "data" / "pokemons-legendary.json"

with RUTA_DATOS.open(encoding="utf-8") as f:
    DATOS = json.load(f)

@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "POST":
        trainer = request.form["trainer"]
        return render_template('listado-pkm.html', pokemons=DATOS, trainer=trainer)
    else:
        return render_template('index.html')
        
@app.route('/pokemons')
def listadoPokemon():
    return render_template('listado-pkm.html', pokemons=DATOS, trainer="trainer")

@app.route('/pokemons/<int:id>')
def pokemon(id):

    pokemon = next((p for p in DATOS if p["id"] == id), None)

    if pokemon is None:
        return "Pokemon no encontrado", 404
    
    return render_template('pokemon.html', pokemon = pokemon)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)