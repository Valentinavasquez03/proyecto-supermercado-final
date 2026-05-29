from flask import Blueprint, render_template, request, redirect, url_for, flash
import database as dbase
from bson.objectid import ObjectId

products_bp = Blueprint('products', __name__)

@products_bp.route('/products/new', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        db = dbase.dbConnection()
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio_raw = request.form.get('precio')
        stock_raw = request.form.get('stock')
        categoria = request.form.get('categoria')
        imagen = request.form.get('imagen', '').strip()

        if not imagen:
            imagen = "https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=150"

        if db is not None:
            db['productos'].insert_one({
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": float(precio_raw),
                "stock": int(stock_raw),
                "categoria": categoria,
                "imagen": imagen
            })
            flash("Producto registrado con éxito.", "success")
        return redirect(url_for('products.create_product'))
    return render_template('create_product.html')

@products_bp.route('/products/search', methods=['GET'])
def search_products():
    db = dbase.dbConnection()
    query_nombre = request.args.get('nombre', '').strip()
    query_categoria = request.args.get('categoria', '').strip()
    query_precio_max = request.args.get('precio_max', '').strip()
    
    filtro = {}
    if query_nombre:
        filtro['nombre'] = {'$regex': query_nombre, '$options': 'i'}
    if query_categoria:
        filtro['categoria'] = query_categoria
    if query_precio_max:
        filtro['precio'] = {'$lte': float(query_precio_max)}

    productos_encontrados = list(db['productos'].find(filtro)) if db is not None else []
    return render_template('search_product.html', productos=productos_encontrados, q_nombre=query_nombre, q_categoria=query_categoria, q_precio_max=query_precio_max)

@products_bp.route('/products/<string:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    db = dbase.dbConnection()
    if request.method == 'POST':
        db['productos'].update_one({"_id": ObjectId(id)}, {"$set": {
            "nombre": request.form.get('nombre'),
            "categoria": request.form.get('categoria'),
            "precio": float(request.form.get('precio')),
            "stock": int(request.form.get('stock')),
            "imagen": request.form.get('imagen'),
            "descripcion": request.form.get('descripcion')
        }})
        flash("Producto actualizado con éxito.", "success")
        return redirect(url_for('products.search_products'))
    
    producto = db['productos'].find_one({"_id": ObjectId(id)})
    return render_template('edit_product.html', producto=producto)

@products_bp.route('/products/<string:id>/delete', methods=['GET', 'POST'])
def delete_product(id):
    db = dbase.dbConnection()
    if request.method == 'POST':
        db['productos'].delete_one({"_id": ObjectId(id)})
        flash("Producto eliminado correctamente.", "success")
        return redirect(url_for('products.search_products'))
    producto = db['productos'].find_one({"_id": ObjectId(id)})
    return render_template('delete_confirm.html', producto=producto)

@products_bp.route('/products/low-stock', methods=['GET'])
def low_stock_products():
    db = dbase.dbConnection()
    criticos = list(db['productos'].find({"stock": {"$lte": 5}})) if db is not None else []
    return render_template('low_stock.html', productos=criticos)
