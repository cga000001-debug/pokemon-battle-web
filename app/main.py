import json
from flask import Flask, render_template, request
from pathlib import Path

app = Flask(__name__)

RUTA_DATOS = Path(__file__).resolve().parent.parent / "data" / "pokemons-legendary.json"

with RUTA_DATOS.open(encoding="utf-8") as f:
    DATOS = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')
        
@app.route('/pokemons', methods=["GET","POST"])
def listadoPokemon():
    if request.method == "POST":
        trainer = request.form["trainer"].strip()
        return render_template('listado-pkm.html', pokemons=DATOS, trainer=trainer)
    else:
        return
        

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

    pokemon = request.form["pokemon"].strip().lower()
    trainer = request.form.get("trainer", "").strip()
    error = None

    if not pokemon:
        error = "El nombre del pokemon es obligatorio"
    elif not any(p["name"] == pokemon for p in DATOS):
        error = "Pokemon no encontrado"

    if error:
        return error

    return render_template('battle.html')

if __name__ == '__main__':
    app.run(port=8080)