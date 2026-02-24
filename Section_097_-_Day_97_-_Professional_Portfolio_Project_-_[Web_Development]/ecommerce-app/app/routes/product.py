from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from app.models import Product
from app.forms import ProductForm
from app.decorators import admin_required

product_bp = Blueprint('product', __name__)

@product_bp.route('/product/<int:product_id>')
def detail(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        abort(404)
    return render_template('product/detail.html', product=product)

@product_bp.route('/admin/product/add', methods=['GET', 'POST'])
@admin_required
def admin_add():
    form = ProductForm()
    if form.validate_on_submit():
        product_id = Product.create(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            image_url=form.image_url.data
        )
        if product_id:
            flash('Product added successfully', 'success')
            return redirect(url_for('product.detail', product_id=product_id))
        else:
            flash('Error adding product', 'error')
    return render_template('product/admin_add.html', form=form)

@product_bp.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        abort(404)
    form = ProductForm()
    if request.method == 'GET':
        # Pre-populate form with existing product data
        form.name.data = product['name']
        form.description.data = product['description']
        form.price.data = product['price']
        form.stock.data = product['stock']
        form.image_url.data = product['image_url']
    if form.validate_on_submit():
        success = Product.update(
            product_id,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            image_url=form.image_url.data
        )
        if success:
            flash('Product updated successfully', 'success')
            return redirect(url_for('product.detail', product_id=product_id))
        else:
            flash('Error updating product', 'error')
    return render_template('product/admin_edit.html', form=form, product=product)

@product_bp.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        abort(404)
    success = Product.delete(product_id)
    if success:
        flash('Product deleted successfully', 'success')
    else:
        flash('Error deleting product', 'error')
    return redirect(url_for('main.index'))