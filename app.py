from flask import Flask, render_template,g, request, redirect, url_for, flash
from datetime import datetime
import sqlite3
from gestor_gastos import gastos_bp,funciones
from config import Config


# Coneccion a la base de datos y cursor


app = Flask(__name__)
app.secret_key = 'clave_temporal'  # Cambia esto
app.config.from_object(Config)

DATABASE = app.config['DATABASE']


@app.teardown_appcontext
def close_db(exc):
    """
    Cierra la conexión al terminar el contexto de la app (fin de la petición).
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

with app.app_context():
         funciones.init_db(DATABASE)

app.register_blueprint(gastos_bp)

@app.route('/')
def home():
    # Opción A: Redirigir al blueprint de gastos
    return redirect(url_for('gastos. index'))

if __name__ == '__main__':
    app.run(debug=True)