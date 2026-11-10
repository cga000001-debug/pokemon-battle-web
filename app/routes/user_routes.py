from flask import Blueprint, redirect, render_template, request, session, url_for
from app.forms.trainer_form import TrainerForm

user_bp = Blueprint("user", __name__)

@user_bp.route('/', methods=["GET","POST"])
def index():
    if "trainer" in session:
        return redirect(url_for('pokemon.listadoPokemon'))

    form = TrainerForm()

    if form.validate_on_submit():
        session["trainer"] = form.trainer.data
        return redirect(url_for('pokemon.listadoPokemon'))

    return render_template('index.html', form=form)


@user_bp.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('user.index'))