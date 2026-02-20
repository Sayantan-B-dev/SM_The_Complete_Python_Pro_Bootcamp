from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Cafe
from .forms import AddCafeForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    cafes = Cafe.query.all()
    return render_template('index.html', cafes=cafes)

@main.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = AddCafeForm()
    if form.validate_on_submit():
        try:
            new_cafe = Cafe(
                name=form.name.data,
                map_url=form.map_url.data,
                img_url=form.img_url.data,
                location=form.location.data,
                has_sockets='TRUE' if form.has_sockets.data else 'FALSE',
                has_toilet='TRUE' if form.has_toilet.data else 'FALSE',
                has_wifi='TRUE' if form.has_wifi.data else 'FALSE',
                can_take_calls='TRUE' if form.can_take_calls.data else 'FALSE',
                seats=form.seats.data,
                coffee_price=str(form.coffee_price.data)  # convert Decimal to string
            )
            db.session.add(new_cafe)
            db.session.commit()
            flash('Cafe added successfully!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding cafe: {str(e)}', 'error')
    else:
        # Form validation failed – flash each error
        for field, errors in form.errors.items():
            for error in errors:
                label = getattr(form, field).label.text
                flash(f'Error in {label}: {error}', 'error')
    return render_template('add.html', form=form)

@main.route('/delete/<int:cafe_id>', methods=['POST'])
def delete_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    db.session.delete(cafe)
    db.session.commit()
    flash('Cafe deleted.', 'info')
    return redirect(url_for('main.index'))