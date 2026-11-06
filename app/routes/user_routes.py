from flask import Blueprint, app, redirect, render_template, request, session, url_for

user_bp = Blueprint("user", __name__)

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

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('index'))