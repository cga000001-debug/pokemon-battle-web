import os
from flask import Flask
from app.routes.pokemon_routes import pokemon_bp
from app.routes.user_routes import user_bp
from app.routes.battle_routes import battle_bp
from flask_session import Session


app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_FILE_DIR"] = "./.flask_session"
app.secret_key = os.environ.get("SECRET_KEY", "clave-solo-para-desarrollo")

Session(app)

app.register_blueprint(user_bp, url_index="/user")
app.register_blueprint(pokemon_bp, url_prefix="/pokemons")
app.register_blueprint(battle_bp, url_prefix="/battle")

if __name__ == '__main__':
    app.run(port=8080)