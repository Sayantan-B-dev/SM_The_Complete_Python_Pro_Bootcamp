from flask import Blueprint, render_template
from app.models import Product

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    products = Product.get_all()
    return render_template('index.html', products=products)