from flask import Flask, render_template,g, request, redirect, url_for, flash
import funciones
from datetime import datetime
import sqlite3

# Coneccion a la base de datos y cursor


app = Flask(__name__)
app.secret_key = 'clave_temporal'  # Cambia esto
DATABASE = 'gastos.db'

# Configuración
file_name_gs = "key.json"
google_sheet = "Contabilidad_personal_v1.3"
sheet_name = "Entrada_datos"


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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resumen', methods=["GET","POST"])
def resumen():
    
    if request.method == "POST":
        if request.form.get("dia"):
            dias = request.form.get("dia")
        elif request.form.get("semana"):
            dias = request.form.get("semana")
            print(dias)
        elif request.form.get("mes"):
            dias = request.form.get("mes")
        else:
            dias = 7
        return redirect(url_for('resumen',dias=dias))
    
    dias = request.args.get('dias', default=7, type=int)

    resultados = funciones.traer_datos(dias)
    return render_template('resumen.html', resultados=resultados, seleccionar_categoria=funciones.seleccionar_categoria)

@app.route('/registrar', methods=['POST'])
def registrar():
    

    try:
        # Obtener datos del formulario
        tipo = request.form['tipo']
        motivo = request.form['motivo']
        monto = float(request.form['monto'])
        descripcion = request.form.get('descripcion', ' ')
        fecha_hora_form = request.form.get('fecha_hora')

        # Debug: imprimir lo que recibimos
        print(f"DEBUG - fecha_hora_form recibido: {fecha_hora_form}")

        # Si no viene fecha/hora del formulario, usar la actual
        if not fecha_hora_form:
            now = datetime.now()
            fecha_hora = now.strftime("%Y-%m-%d %H:%M:%S")
        else:
            # Convertir el formato del formulario (YYYY-MM-DDTHH:MM) a nuestro formato
            try:
                # Reemplazar 'T' por espacio y agregar segundos
                fecha_hora = fecha_hora_form.replace('T', ' ') + ':00'
            except Exception as e:
                print(f"Error procesando fecha: {e}")
                # Fallback: usar fecha actual
                now = datetime.now()
                fecha_hora = now.strftime("%Y-%m-%d %H:%M:%S")

        # Validaciones básicas
        if monto <= 0:
            flash('❌ El monto debe ser mayor a 0', 'error')
            return redirect(url_for('index'))

        # Si es gasto, hacer negativo el monto
        if tipo == 'Gasto':
            monto = -abs(monto)

        values = [[fecha_hora, tipo, motivo, monto, descripcion]]
        
        # Escribir en la base de datos: usar conexión por petición (get_db)
        db = get_db()
        cursor = db.cursor()
        cursor.executemany("INSERT INTO datos VALUES (?,?,?,?,?)", values)
        db.commit()

        flash(f'✅ {tipo} registrado correctamente!', 'success')

    except ValueError as e:
        flash('❌ El monto debe ser un número válido', 'error')
        print(f"ValueError: {e}")
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'error')
        print(f"Error general: {e}")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)