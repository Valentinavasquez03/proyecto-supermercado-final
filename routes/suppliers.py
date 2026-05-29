from flask import Blueprint, render_template, request, redirect, url_for, flash
import database as dbase

suppliers_bp = Blueprint('suppliers', __name__)

@suppliers_bp.route('/suppliers/list', methods=['GET', 'POST'])
def list_suppliers():
    db = dbase.dbConnection()
    
    # Si se envía el formulario, guarda el proveedor aquí directamente
    if request.method == 'POST':
        if db is not None:
            db['proveedores'].insert_one({
                "nombre_proveedor": request.form.get('nombre_proveedor'),
                "telefono": request.form.get('telefono')
            })
            flash("Proveedor guardado exitosamente.", "success")
        return redirect(url_for('suppliers.list_suppliers'))

    # Carga la lista
    lista = list(db['proveedores'].find()) if db is not None else []
    return render_template('list_suppliers.html', proveedores=lista)