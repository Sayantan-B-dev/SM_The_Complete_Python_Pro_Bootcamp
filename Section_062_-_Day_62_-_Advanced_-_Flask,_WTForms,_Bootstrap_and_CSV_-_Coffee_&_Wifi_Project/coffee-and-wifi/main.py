from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, URLField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# Map numeric ratings to emoji strings
COFFEE_CHOICES = [('0', '✘'), ('1', '☕️'), ('2', '☕☕'), ('3', '☕☕☕'), ('4', '☕☕☕☕'), ('5', '☕☕☕☕☕')]
WIFI_CHOICES = [('0', '✘'), ('1', '💪'), ('2', '💪💪'), ('3', '💪💪💪'), ('4', '💪💪💪💪'), ('5', '💪💪💪💪💪')]
POWER_CHOICES = [('0', '✘'), ('1', '🔌'), ('2', '🔌🔌'), ('3', '🔌🔌🔌'), ('4', '🔌🔌🔌🔌'), ('5', '🔌🔌🔌🔌🔌')]


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location URL', validators=[DataRequired(), URL()])
    open_time = StringField('Open Time (e.g., 8AM)', validators=[DataRequired()])
    close_time = StringField('Close Time (e.g., 5PM)', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=COFFEE_CHOICES, validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Rating', choices=WIFI_CHOICES, validators=[DataRequired()])
    power_rating = SelectField('Power Outlet Rating', choices=POWER_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Add Cafe')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Gather form data
        cafe_data = [
            form.cafe.data,
            form.location.data,
            form.open_time.data,
            form.close_time.data,
            COFFEE_CHOICES[int(form.coffee_rating.data)][1],
            WIFI_CHOICES[int(form.wifi_rating.data)][1],
            POWER_CHOICES[int(form.power_rating.data)][1]
        ]
        print(cafe_data)
        # Append to CSV file
        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(cafe_data)
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]
    return render_template('cafes.html', cafes=list_of_rows)

@app.route('/delete/<int:cafe_id>', methods=['POST'])
def delete_cafe(cafe_id):
    with open('cafe-data.csv', mode='r', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]
    list_of_rows.pop(cafe_id+1)
    with open('cafe-data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(list_of_rows)
    return redirect(url_for('cafes'))




if __name__ == '__main__':
    app.run(debug=True)