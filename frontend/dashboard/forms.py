from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class AddDamageTypeForm(FlaskForm):
    def __init__(self, choices, *args, **kwargs):
        super(AddDamageTypeForm, self).__init__(*args, **kwargs)
        self.damage_type.choices = choices

    damage_type = SelectField('Select Damage Type')
    submit = SubmitField('Submit')
