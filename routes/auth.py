from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'admin123':
            # CORRECCIÓN: Te redirige directo a registrar producto (HU02) en lugar de buscar
            return redirect(url_for('products.create_product'))
        flash("Credenciales incorrectas.", "danger")
    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    return redirect(url_for('auth.login'))