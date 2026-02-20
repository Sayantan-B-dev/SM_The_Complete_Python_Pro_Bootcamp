from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL, Optional

class AddCafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    map_url = StringField('Google Maps URL', validators=[URL(), Optional()])
    img_url = StringField('Image URL', validators=[URL(), Optional()])
    location = StringField('Location', validators=[DataRequired()])
    has_sockets = BooleanField('Has Sockets')
    has_toilet = BooleanField('Has Toilet')
    has_wifi = BooleanField('Has WiFi')
    can_take_calls = BooleanField('Can Take Calls')
    seats = SelectField('Seats', choices=[
        ('0-10', '0-10'), ('10-20', '10-20'), ('20-30', '20-30'),
        ('30-40', '30-40'), ('40-50', '40-50'), ('50+', '50+')
    ], validators=[DataRequired()])
    coffee_price = DecimalField('Coffee Price (£)', places=2, validators=[DataRequired()])
    submit = SubmitField('Add Cafe')