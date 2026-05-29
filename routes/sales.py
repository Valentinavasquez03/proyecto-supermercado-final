from flask import Blueprint, render_template, request, redirect, url_for, flash
import database as dbase
from bson.objectid import ObjectId
from datetime import datetime

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/sales/new', methods=['GET', 'POST'])
def create_sale():
    db = dbase.dbConnection()
    if request.method == 'POST':
        producto_id = request.form.get('producto_id')
        cantidad = int(request.form.get('cantidad', 1))
        descuento = float(request.form.get('descuento', 0))

        producto = db['productos'].find_one({"_id": ObjectId(producto_id)})
        if producto and producto['stock'] >= cantidad:
            total = round((producto['precio'] * cantidad) * (1 - (descuento / 100)), 2)
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")

            db['ventas'].insert_one({
                "producto_id": ObjectId(producto_id),
                "producto_nombre": producto['nombre'],
                "cantidad": cantidad,
                "descuento": descuento,
                "total": total,
                "fecha": fecha_hoy
            })
            db['productos'].update_one({"_id": ObjectId(producto_id)}, {"$set": {"stock": producto['stock'] - cantidad}})
            flash("Venta registrada exitosamente.", "success")
        else:
            flash("Error: Stock insuficiente para realizar la venta.", "danger")
        return redirect(url_for('sales.create_sale'))

    # VARIABLES EXACTAS ENVIADAS A LA PLANTILLA
    productos = list(db['productos'].find()) if db is not None else []
    ventas = list(db['ventas'].find().sort("_id", -1)) if db is not None else []
    return render_template('nueva_venta.html', productos=productos, ventas=ventas)

@sales_bp.route('/sales/report', methods=['GET'])
def sales_report():
    db = dbase.dbConnection()
    fecha_filtro = request.args.get('fecha_filtro', datetime.now().strftime("%Y-%m-%d"))
    
    # Busca las ventas de la fecha seleccionada
    ventas = list(db['ventas'].find({"fecha": fecha_filtro})) if db is not None else []
    
    total_recaudado = sum(float(v['total']) for v in ventas)
    total_articulos = sum(int(v['cantidad']) for v in ventas)
    
    # VARIABLES EXACTAS ENVIADAS A LA PLANTILLA DE REPORTES
    return render_template('sales_report.html', ventas=ventas, total_recaudado=total_recaudado, total_articulos=total_articulos, fecha_actual=fecha_filtro)