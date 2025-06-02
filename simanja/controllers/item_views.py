from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from simanja.models import item as item_model

from functools import wraps

item_bp = Blueprint('item', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@item_bp.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    message = None
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        category_alias = request.form.get('category_alias')
        category_code = request.form.get('category_code')
        if category_name and category_alias:
            success = item_model.create_category(category_name, category_alias, category_code)
            if success:
                return redirect(url_for('item.category'))
            else:
                message = "Category sudah ada atau error saat input."
        else:
            message = "Nama kategory dan Kode harus diisi."
    categories = item_model.get_all_categories() 
    return render_template('items/category.html', categories=categories, message=message)

@item_bp.route('/category/edit', methods=['POST'])
@login_required
def edit_category():
    category_id = request.form.get('category_id')
    category_name = request.form.get('category_name')
    category_alias = request.form.get('category_alias')
    category_code = request.form.get('category_code')

    if category_id and category_name and category_alias:
        success = item_model.update_category(category_id, category_name, category_alias, category_code)
        if success:
            flash("Kategori berhasil diupdate.", "success")
        else:
            flash("Gagal mengupdate kategori.", "danger")
    else:
        flash("Data tidak lengkap untuk update.", "warning")

    return redirect(url_for('item.category'))


@item_bp.route('/category/delete', methods=['POST'])
@login_required
def delete_category():
    category_id = request.form.get('category_id')
    print(f"Category ID: {category_id}")
    if category_id:
        success = item_model.delete_category_by_id(category_id)
        if success:
            flash("Kategori berhasil dihapus.", "success")
        else:
            flash("Gagal menghapus kategori.", "danger")
    else:
        flash("ID kategori tidak ditemukan dalam request.", "warning")
    return redirect(url_for('item.category'))

@item_bp.route('/item', methods=['GET', 'POST'])
def item():
    message = None
    if request.method == 'POST':
        item_name = request.form.get('item_name')
        category_id_item = request.form.get('category_id_item')
        received_date = request.form.get('received_date')
        status_id_item = request.form.get('status_id_item')
        takeout_date = request.form.get('takeout_date')

        if item_name and category_id_item and received_date and status_id_item:
            success = item_model.create_item(
                item_name=item_name,
                category_id_item=category_id_item,
                received_date=received_date,
                status_id_item=status_id_item,
                takeout_date=takeout_date
            )
            if success:
                return redirect(url_for('item.item'))
            else:
                message = "Gagal menyimpan data item."
        else:
            message = "Semua field wajib diisi kecuali takeout_date."

    items = item_model.get_all_items()
    categories = item_model.get_all_categories() 
    statuses= item_model.get_all_status()
    return render_template('items/item.html', items=items, categories=categories, statuses=statuses, message=message)

@item_bp.route('/item/edit', methods=['POST'])
@login_required
def edit_item():
    item_id = request.form.get('item_id')
    item_name = request.form.get('item_name')
    category_id_item = request.form.get('category_id_item')
    received_date = request.form.get('received_date')
    status_id_item = request.form.get('status_id_item')
    location_id_name = request.form.get('location_id_name')
    take_out_date = request.form.get('take_out_date')
    end_date = request.form.get('end_date')

    if item_id and item_name:
        success = item_model.update_item(
            item_id, item_name, category_id_item,
            received_date, status_id_item,
            location_id_name, take_out_date, end_date
        )
        if success:
            flash("Item berhasil diupdate.", "success")
        else:
            flash("Gagal mengupdate item.", "danger")
    else:
        flash("Data tidak lengkap untuk update.", "warning")

    return redirect(url_for('item.item'))

@item_bp.route('/item/delete', methods=['POST'])
@login_required
def delete_item():
    item_id = request.form.get('item_id')
    print(f"Item ID: {item_id}")
    if item_id:
        success = item_model.delete_item_by_id(item_id)
        if success:
            flash("Item berhasil dihapus.", "success")
        else:
            flash("Gagal menghapus item.", "danger")
    else:
        flash("ID item tidak ditemukan dalam request.", "warning")
    return redirect(url_for('item.item'))