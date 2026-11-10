from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class TrainerForm(FlaskForm):
    trainer = StringField(
        "Trainer:",
        validators=[
            DataRequired(message="El trainer es obligatorio."),
            Length(min=3, max=15, message="El trainer debe tener entre 3 y 15 caracteres."),
        ],
    )