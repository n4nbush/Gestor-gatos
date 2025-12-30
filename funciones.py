from datetime import time, datetime
import sqlite3, shutil, json 

grupos={
    "🧾 Finanzas y Deudas":["Deuda Viejo","Tarjeta Visa","Tarjeta Master","Deuda Banco"],
    "🛒 Consumo y Vida Diaria":["Gastos Hormiga", "Comida Trabajo","Almacén"],
    "🏠 Hogar y Servicios":["Internet","Celular","Ferretería","Luz","Servicios Digitales"],
    "👨‍👩‍👦 Familia":["Niñera","Boris","Agustina"],
    "🧍‍♂️ Bienestar y Personales":["Gustos","Ropa","GIM","Farmacia","Psicóloga","Peluquería","Indoor"],
    "🚗 Transporte y Movilidad":["Uber","Moto","Clio","SUBE"]
}


def traer_datos(dias=60):
    conn = sqlite3.connect('gastos.db')

    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM datos
        WHERE date(FECHA) >= date ('now',?)
        order by FECHA DESC

                
    """,(f'-{dias} day',))

    resultados = cursor.fetchall()
    return(resultados)

def seleccionar_categoria(categoria):

    for nombre_grupo, lista_categorias in grupos.items():
        if categoria in lista_categorias:
            return (nombre_grupo)
    
def procesado_fecha(fecha):
    fecha = fecha.replace("-","/")
    dt = datetime.strptime(fecha,"%d/%m/%Y %H:%M:%S")
    
    fechas = [dt.day,dt.month,dt.year]

    return(fechas)




def backup():
    ahora = datetime.now()


    try:
        with open('fecha_ultimo_backup.json','r') as f:
            fecha_str = json.load(f)
            fecha_ultimo_backup = datetime.fromisoformat(fecha_str)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        print("Archivo json de fecha backup no existe, creando uno nuevo")
        fecha_ultimo_backup = datetime.now()
        with open('fecha_ultimo_backup.json', 'w', encoding='utf-8') as archivo:
            json.dump(fecha_ultimo_backup.isoformat(), archivo, indent=4, ensure_ascii=False)
            nombre_backup=f"gastos_{ahora.strftime('%Y-%m-%d_%H-%M')}.db"
            shutil.copy2("gastos.db",nombre_backup)


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

listado = resumen_grupos()


for nombre,total in listado["🛒 Consumo y Vida Diaria"].items():
    print (nombre,total)
