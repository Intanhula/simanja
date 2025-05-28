from flask import Blueprint, render_template, redirect, url_for, request, session
from simanja.models import item as item_model

item_bp = Blueprint('item', __name__)
@item_bp.route('/category', methods=['GET', 'POST'])
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
    return render_template('items/item.html', items=items, message=message)
