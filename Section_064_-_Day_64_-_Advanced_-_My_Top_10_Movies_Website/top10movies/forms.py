from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class RateMovieForm(FlaskForm):
    rating = FloatField(
        "Your Rating Out of 10 e.g. 7.5",
        validators=[
            DataRequired(message="Rating is required."),
            NumberRange(min=0, max=10, message="Rating must be between 0 and 10.")
        ]
    )
    review = StringField(
        "Your Review",
        validators=[
            DataRequired(message="Review cannot be empty."),
            Length(min=1, max=250, message="Review must be between 1 and 250 characters.")
        ]
    )
    submit = SubmitField("Done")

class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Search Movie")