from flask import Flask, redirect, url_for
import database as dbase
from routes.auth import auth_bp
from routes.products import products_bp
from routes.sales import sales_bp
from routes.suppliers import suppliers_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(suppliers_bp)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)