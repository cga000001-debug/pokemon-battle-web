import json
from flask import Flask, render_template
from pathlib import Path

app = Flask(__name__)

RUTA_DATOS = Path(__file__).resolve().parent.parent / "data" / "pokemons-legendary.json"

with RUTA_DATOS.open(encoding="utf-8") as f:
    DATOS = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/listado-pkm/')
def listadoPokemon():
    return render_template('listado-pkm.html', id=id, DATOS=DATOS)

#@app.route('/listado-pkm/{id}')
#def listadoPokemon():
#    return render_template('pokemon.html')

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)