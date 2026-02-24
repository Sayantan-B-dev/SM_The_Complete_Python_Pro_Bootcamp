import razorpay
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from flask_login import login_required, current_user
from app.models import Cart, Product, get_db
from app.routes.cart import get_current_cart_id

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/checkout')
@login_required
def checkout():
    cart_id = get_current_cart_id()
    items, total = Cart.get_cart_items(cart_id)
    if not items:
        flash('Your cart is empty', 'info')
        return redirect(url_for('cart.view_cart'))
    
    # Check stock sufficiency
    for item in items:
        product = Product.get_by_id(item['product_id'])
        if product['stock'] < item['quantity']:
            flash(f"Insufficient stock for {item['name']}. Available: {product['stock']}", 'error')
            return redirect(url_for('cart.view_cart'))
    
    # Create Razorpay order
    client = razorpay.Client(auth=(
        current_app.config['RAZORPAY_KEY_ID'], 
        current_app.config['RAZORPAY_KEY_SECRET']
    ))
    order_data = {
        'amount': int(total * 100),
        'currency': 'INR',
        'receipt': f'cart_{cart_id}',
        'payment_capture': 1
    }
    order = client.order.create(order_data)
    
    # Store order in DB
    db = get_db()
    cursor = db.execute(
        'INSERT INTO orders (user_id, total_amount, razorpay_order_id) VALUES (?, ?, ?)',
        (current_user.id, total, order['id'])
    )
    order_id = cursor.lastrowid
    db.commit()
    session['current_order_id'] = order_id
    
    return render_template('cart/checkout.html', order=order, items=items, total=total,
                         key_id=current_app.config['RAZORPAY_KEY_ID'])

@payment_bp.route('/payment/success', methods=['POST'])
@login_required
def payment_success():
    client = razorpay.Client(auth=(
        current_app.config['RAZORPAY_KEY_ID'], 
        current_app.config['RAZORPAY_KEY_SECRET']
    ))
    params = {
        'razorpay_order_id': request.form['razorpay_order_id'],
        'razorpay_payment_id': request.form['razorpay_payment_id'],
        'razorpay_signature': request.form['razorpay_signature']
    }
    try:
        client.utility.verify_payment_signature(params)
        db = get_db()
        order_id = session.get('current_order_id')
        if order_id:
            db.execute('UPDATE orders SET status = ? WHERE id = ?', ('paid', order_id))
            
            # Insert order items and reduce stock
            cart_id = get_current_cart_id()
            items, _ = Cart.get_cart_items(cart_id)
            for item in items:
                # Insert into order_items
                db.execute(
                    'INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                    (order_id, item['product_id'], item['quantity'], item['price'])
                )
                # Reduce stock
                Product.update_stock(item['product_id'], item['quantity'])
            
            # Clear cart
            db.execute('DELETE FROM cart_items WHERE cart_id = ?', (cart_id,))
            db.commit()
            flash('Payment successful! Your order is confirmed.', 'success')
            session.pop('current_order_id', None)
            return redirect(url_for('main.index'))
        else:
            flash('Order not found', 'error')
    except Exception as e:
        flash('Payment verification failed', 'error')
        current_app.logger.error(f'Payment error: {e}')
    return redirect(url_for('cart.view_cart'))