from flask import Blueprint, render_template
from app.models import Product
from app.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@admin_required
def dashboard():
    products = Product.get_all()
    return render_template('admin/dashboard.html', products=products)