from datetime import time, datetime
import sqlite3, shutil, json, os
from flask import Flask, render_template,g, request, redirect, url_for, flash
from config import Config
from contextlib import closing

grupos={
    "🧾 Finanzas y Deudas":["Deuda Viejo","Tarjeta Visa","Tarjeta Master","Deuda Banco"],
    "🛒 Consumo y Vida Diaria":["Gastos Hormiga", "Comida Trabajo","Almacén"],
    "🏠 Hogar y Servicios":["Internet","Celular","Ferretería","Luz","Servicios Digitales"],
    "👨‍👩‍👦 Familia":["Niñera","Boris","Agustina"],
    "🧍‍♂️ Bienestar y Personales":["Gustos","Ropa","GIM","Farmacia","Psicóloga","Peluquería","Indoor"],
    "🚗 Transporte y Movilidad":["Uber","Moto","Clio","SUBE"],
    "Otros Gastos":["Otros Gastos"],
    "Ingresos":["Salario","Inversiones","Regalo","Reembolso","Otros Ingresos"]
}

categorias = ['Internet','Luz','Celular','Ferretería','Servicios Digitales','Moto','SUBE','Uber','Clio','Deuda Viejo','Tarjeta Master','Tarjeta Visa','Deuda Banco','Almacén','Comida Trabajo','Gastos Hormiga','Agustina','Boris','Niñera','Ropa','Psicóloga','Gustos','Peluquería','GIM','Indoor','Otros gastos','Farmacia']

DATABASE = Config.DATABASE

def init_db(DATABASE):
    """
    Crea la tabla 'datos' si no existe. Llamar manualmente si la DB no está creada.
    """
    os.makedirs(Config.DATABASE_FOLDER, exist_ok=True)

    db = sqlite3.connect(DATABASE)
    try:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS datos_crudos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                FECHA TEXT,
                TIPO TEXT,
                METODO_PAGO TEXT,
                CATEGORIA TEXT,
                IMPORTE REAL,
                DESCRIPCION TEXT
            )
        """)
        db.commit()
    finally:
        db.close()

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

def traer_datos(dias=60,DATABASE=DATABASE):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM datos_crudos WHERE fecha >= date('now', '-{dias} days') ORDER BY fecha DESC")

    resultados = cursor.fetchall()
    return(resultados)

def seleccionar_categoria(categoria):

    for nombre_grupo, lista_categorias in grupos.items():
        if categoria in lista_categorias:
            return (nombre_grupo)
    
def procesado_fecha(fecha):
    fecha = fecha.replace("T", " ")
    formatos = ['%Y-%m-%d %H:%M:%S',
                '%d/%m/%Y %H:%M:%S',
                '%Y-%m-%d %H:%M',
                '%d-%m-%Y %H:%M:%S']
    dt = None
    for formato in formatos:
        try:
            dt = datetime.strptime(fecha.strip(), formato)
            break
        except ValueError:
            continue
    if dt is None:
        print(f"No se pudo parsear la fecha: {fecha}")
        return fecha
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def backup():
    ahora = datetime.now()
    os.makedirs('gestor_gastos/backup', exist_ok=True)

    try:
        with open(Config.BACKUP,'r') as f:
            fecha_str = json.load(f)
            fecha_ultimo_backup = datetime.fromisoformat(fecha_str)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        print("Archivo json de fecha backup no existe, creando uno nuevo")
        fecha_ultimo_backup = datetime.now()
        with open(Config.BACKUP, 'w', encoding='utf-8') as archivo:
            json.dump(fecha_ultimo_backup.isoformat(), archivo, indent=4, ensure_ascii=False)
            nombre_backup=f"gestor_gastos/backup/gastos_{ahora.strftime('%Y-%m-%d_%H-%M')}.db"
            shutil.copy2(DATABASE,nombre_backup)


    diff = ahora - fecha_ultimo_backup
    diff = diff.days


    if diff > 15:
        print("Creando nuevo backup")
        nombre_backup=f"gastos_{ahora.datetimestr('%Y-%m-%d_%H-%M')}.db"
        shutil.copy2("gastos.db",nombre_backup)
        fecha_ultimo_backup=datetime.now()
        print("Actualizando fecha del ultimo backup")
        with open('fecha_ultimo_backup.json', 'w', encoding='utf-8') as archivo:
            json.dump(fecha_ultimo_backup.isoformat(), archivo, indent=4, ensure_ascii=False)

def resumen_grupos(dias=30):
    listado=traer_datos(dias)
    totales = {}
    for x in listado:
        categoria = x[2]

        for nombre_grupo, lista_categoria in grupos.items():
            if categoria in lista_categoria:    
                monto = x[3]
                for char in ["$",",","-"," "]:
                    monto = monto.replace(char,"")
                monto = float(monto)

                if nombre_grupo not in totales:
                    totales[nombre_grupo] = {}
                    totales[nombre_grupo]["Total"] = 0

                if categoria not in totales[nombre_grupo]:
                    totales[nombre_grupo][categoria] = 0
                    
                totales[nombre_grupo]["Total"] += monto
                totales[nombre_grupo][categoria] += monto
                    
                break
    
    return totales

def asignar_grupos(categoria):
    
    for nombre_grupo,lista_categoria in grupos.items():
        if categoria in lista_categoria:
            return(nombre_grupo)

def limpiar_monto(monto):
    for char in ["$",",","-"," "]:
        monto = monto.replace(char,"")
    return float(monto)

def filtrar(dias=30,grupo_select=None,categoria_select=None):
    listado=(traer_datos(dias))
    resultados=[]
    total = {
        "Total general":0,
        "🧾 Finanzas y Deudas":0,
        "🛒 Consumo y Vida Diaria":0,
        "🏠 Hogar y Servicios":0,
        "👨‍👩‍👦 Familia":0,
        "🧍‍♂️ Bienestar y Personales":0,
        "Otros Gastos":0,
        "Ingresos":0
    }
    for id,fecha,tipo,mpago,categoria,monto,descripcion in listado:
        grupo = seleccionar_categoria(categoria)
        if grupo_select is not None and grupo != grupo_select:
            continue
        if categoria_select is not None and categoria != categoria_select:
            continue
        mpago=mpago
        if grupo in total:
            total[grupo] += monto
        total["Total general"] += monto
        resultados.append([id,fecha,tipo,mpago,categoria,grupo,monto,descripcion])
    return(resultados,total)

def procesar_datos(listado):
    
    resultado = []
    for i in listado:
        fecha = procesado_fecha(i[0])
        tipo = i[1]
        if i[1] == "Tarjeta":
            tipo = "Gasto"
            metodo_pago = "Tarjeta"
        else:
            metodo_pago = "Debito"
        grupo = asignar_grupos(i[2])
        categoria = i[2]
        monto = limpiar_monto(i[3])
        descripcion = i[4]
        resultado.append([fecha,tipo,metodo_pago,categoria,monto,descripcion])
    return(resultado)

def obtener_datos(tabla):
    import sqlite3
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM {tabla}")
    datos = cursor.fetchall()
    
    conn.close()
    return datos

def cargar_db(fecha,tipo,mpago,categoria,monto,desc):
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        cursor.executemany("INSERT INTO datos_crudos VALUES (?,?,?,?,?,?)", fecha,tipo,mpago,categoria,monto,desc)
        db.commit()

def borrar_tabla(tabla):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Sentencia SQL para borrar la tabla 'usuarios'
    # La cláusula IF EXISTS es opcional, evita errores si la tabla no existe
    cursor.execute(f'DROP TABLE IF EXISTS "{tabla}"')
    # Confirmar los cambios
    conn.commit()

    # Cerrar la conexión
    conn.close()
    print(f'Tabla{tabla}eliminada exitosamente')

def cargar_db(datos, DATABASE):
    conn = sqlite3.connect(DATABASE)
    try:
        conn.executemany(
            """INSERT INTO datos_crudos 
               (FECHA, TIPO, METODO_PAGO, CATEGORIA, IMPORTE, DESCRIPCION) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            datos
        )
        conn.commit()
    finally:
        conn. close()


def borrar_id(id):
    conn = sqlite3.connect(DATABASE)
    try:
            
            query = f"DELETE FROM datos_crudos WHERE id = {id} ;" 
            conn.execute(query)
            conn.commit()
    finally:
            conn. close()

