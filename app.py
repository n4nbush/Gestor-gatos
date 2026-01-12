from flask import Flask, render_template,g, request, redirect, url_for, flash
from datetime import datetime
import sqlite3
from gestor_gastos import gastos_bp


# Coneccion a la base de datos y cursor


app = Flask(__name__)
app.secret_key = 'clave_temporal'  # Cambia esto
DATABASE = 'data_base/gastos.db'



def get_db():
    """
    Obtiene (o crea) una conexión a la base de datos por contexto de petición.
    No se comparte la conexión entre hilos.
    """
    if 'db' not in g:
        # puedes añadir detect_types o timeout si lo necesitas
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        # opcional: filas como dict
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exc):
    """
    Cierra la conexión al terminar el contexto de la app (fin de la petición).
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """
    Crea la tabla 'datos' si no existe. Llamar manualmente si la DB no está creada.
    """
    db = sqlite3.connect(DATABASE)
    try:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS datos (
                FECHA TEXT,
                TIPO TEXT,
                MOTIVO TEXT,
                IMPORTE REAL,
                DESCRIPCION TEXT
            )
        """)
        db.commit()
    finally:
        db.close()

with app.app_context():
         init_db()

app.register_blueprint(gastos_bp)

@app.route('/')
def home():
    # Opción A: Redirigir al blueprint de gastos
    from flask import redirect, url_for
    return redirect(url_for('gastos. index'))

if __name__ == '__main__':
    app.run(debug=True)