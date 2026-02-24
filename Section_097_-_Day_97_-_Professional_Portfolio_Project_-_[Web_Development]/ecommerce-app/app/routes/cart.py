from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from flask_login import current_user
from app.models import Cart, Product
from app.utils import generate_session_id

cart_bp = Blueprint('cart', __name__)

def get_current_cart_id():
    if current_user.is_authenticated:
        return Cart.get_or_create_cart(user_id=current_user.id)
    else:
        if 'session_id' not in session:
            session['session_id'] = generate_session_id()
        return Cart.get_or_create_cart(session_id=session['session_id'])

@cart_bp.route('/cart')
def view_cart():
    cart_id = get_current_cart_id()
    items, total = Cart.get_cart_items(cart_id)
    return render_template('cart/cart.html', items=items, total=total)

@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart_id = get_current_cart_id()
    quantity = int(request.form.get('quantity', 1))
    success = Cart.add_item(cart_id, product_id, quantity)
    if success:
        flash('Item added to cart', 'success')
    else:
        flash('Unable to add item (out of stock or invalid)', 'error')
    return redirect(request.referrer or url_for('product.detail', product_id=product_id))

@cart_bp.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    cart_id = get_current_cart_id()
    quantity = int(request.form.get('quantity', 1))
    success = Cart.update_item_quantity(cart_id, product_id, quantity)
    if success:
        flash('Cart updated', 'success')
    else:
        flash('Update failed (stock limit)', 'error')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart_id = get_current_cart_id()
    Cart.remove_item(cart_id, product_id)
    flash('Item removed', 'info')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/count')
def cart_count():
    cart_id = get_current_cart_id()
    items, _ = Cart.get_cart_items(cart_id)
    count = sum(item['quantity'] for item in items)
    return jsonify({'count': count})