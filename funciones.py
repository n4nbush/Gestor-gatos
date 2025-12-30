from datetime import time, datetime
import sqlite3, shutil, json 


Finanzas_y_Deudas = ["Deuda Viejo","Tarjeta Visa","Tarjeta Master","Deuda Banco"] 
Consumo_y_Vida_Diaria = ["Gastos Hormiga", "Comida Trabajo","Almacén"]
Hogar_y_Servicios = ["Internet","Celular","Ferretería","Luz","Servicios Digitales"]
Familia = ["Niñera","Boris","Agustina"]
Bienestar_y_Personales = ["Gustos","Ropa","GIM","Farmacia","Psicóloga","Peluquería","Indoor"]
Transporte_y_Movilidad = ["Uber","Moto","Clio","SUBE"]



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

    if categoria in Finanzas_y_Deudas:
        return("🧾 Finanzas y Deudas")
    elif categoria in Consumo_y_Vida_Diaria:
        return("🛒 Consumo y Vida Diaria")
    elif categoria in Hogar_y_Servicios:
        return("🏠 Hogar y Servicios")
    elif categoria in Familia:
        return("👨‍👩‍👦 Familia")
    elif categoria in Bienestar_y_Personales:
        return("🧍‍♂️ Bienestar y Personales")
    elif categoria in Transporte_y_Movilidad:
        return("🚗 Transporte y Movilidad")
    
def procesado_fecha(fecha):
    fecha = fecha.replace("-","/")
    dt = datetime.strptime(fecha,"%d/%m/%Y %H:%M:%S")
    
    fechas = [dt.day,dt.month,dt.year]

    return(fechas)


def procesamiento_de_datos():

    conn = sqlite3.connect('gastos.db')

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM datos
        order by FECHA DESC       
    """)

    resultados = cursor.fetchall()
    return(resultados)

#lista_db=(procesamiento_de_datos())



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



    print(fecha_ultimo_backup)

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
