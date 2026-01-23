from flask import Flask, render_template,g, request, redirect, url_for, flash, current_app
from .  import gastos_bp  # Importar el blueprint del __init__. py
import datetime
# Opción A: Si moviste funciones.py a gastos/
import funciones
from config import Config

DATABASE = Config.DATABASE


@gastos_bp.route('/')
def index():
    
    funciones.backup()
    return render_template('index.html')

@gastos_bp.route('/movimientos', methods=["GET","POST"])
def movimientos():
    
    if request.method == "POST":
        if request.form.get("filtro_fecha"):
            dias = request.form.get("filtro_fecha")
        else:
            dias = 30
        categoria = request.form.get('categoria')
        grupo = request.form.get('grupo')
        return redirect(url_for('gastos.movimientos',dias=dias,categoria=categoria,grupo=grupo))
    
    dias = request.args.get('dias', default=30, type=int)
    categoria = request.args.get('categoria', default=None)
    grupo = request.args.get('grupo', default=None)
    if categoria == "":
        categoria = None
    if grupo == "":
        grupo = None

    resultados,total = funciones.filtrar(dias,categoria_select=categoria,grupo_select=grupo)
    return render_template('movimientos.html', resultados=resultados, seleccionar_categoria=funciones.seleccionar_categoria, categorias=funciones.categorias, categoria=categoria, total=total,grupos=funciones.grupos.keys())

@gastos_bp.route('/borrar',methods=['POST'])
def borrar_movimiento():
    try:
        id = request.form['id']
    except:
        print("Error")

    funciones.borrar_id(id)

    return redirect(url_for('gastos.movimientos'))    


@gastos_bp.route('/registrar', methods=['POST'])
def registrar():
    

    try:
        # Obtener datos del formulario
        tipo = request.form['tipo']
        metodo_pago = request.form['metodo_pago']
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
        

        values = [[fecha_hora, tipo,metodo_pago, motivo, monto, descripcion]]
        
        # Escribir en la base de datos: usar conexión por petición (get_db)
        funciones.cargar_db(values,Config.DATABASE)

        flash(f'✅ {tipo} registrado correctamente!', 'success')

    except ValueError as e:
        flash('❌ El monto debe ser un número válido', 'error')
        print(f"ValueError: {e}")
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'error')
        print(f"Error general: {e}")

    return redirect(url_for('gastos.index'))


@gastos_bp.route('/resumen_grupos', methods=["GET","POST"])
def resumen_cat():
    resumen, total = funciones.filtrar()
    grupos = list(total.keys())
    print(grupos[2])
    return render_template('resumen_grupos.html',total=total,grupos=grupos)

