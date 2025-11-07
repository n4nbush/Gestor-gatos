from flask import Flask, render_template, request, redirect, url_for, flash
from funciones import GoogleSheet
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_temporal'  # Cambia esto

# Configuración
file_name_gs = "key.json"
google_sheet = "Contabilidad_personal_v1.3"
sheet_name = "Entrada_datos"

try:
    google = GoogleSheet(file_name_gs, google_sheet, sheet_name)
    print("✅ Google Sheets conectado correctamente")
except Exception as e:
    print(f"❌ Error conectando Google Sheets: {e}")
    google = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    if google is None:
        flash('❌ Error de conexión con Google Sheets', 'error')
        return redirect(url_for('index'))

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

        # Escribir en Sheets
        rango = google.get_last_row_range()
        google.write_data(rango, values)

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