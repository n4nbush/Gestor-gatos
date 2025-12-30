import gspread
from datetime import time, datetime
import sqlite3


Finanzas_y_Deudas = ["Deuda Viejo","Tarjeta Visa","Tarjeta Master","Deuda Banco"] 
Consumo_y_Vida_Diaria = ["Gastos Hormiga", "Comida Trabajo","Almacén"]
Hogar_y_Servicios = ["Internet","Celular","Ferretería","Luz","Servicios Digitales"]
Familia = ["Niñera","Boris","Agustina"]
Bienestar_y_Personales = ["Gustos","Ropa","GIM","Farmacia","Psicóloga","Peluquería","Indoor"]
Transporte_y_Movilidad = ["Uber","Moto","Clio","SUBE"]

class GoogleSheet:

    def __init__(self,file_name,document,sheet_name):
        self.gc = gspread.service_account(filename=file_name)
        self.sh = self.gc.open(document)
        self.sheet = self.sh.worksheet(sheet_name)

    def get_last_row_range(self):   
        last_row = len(self.sheet.get_all_values()) + 1
        deta = self.sheet.get_values()
        range_start = f"A{last_row}"
        range_end = f"{chr(ord('A') + len(deta[0]) - 1)}{last_row}"
        return f"{range_start}:{range_end}"

    def get_all_values(self):
        #self.sheet.get_all_values () # this return a list of list, so the get all records is easier to get values filtering
        return self.sheet.get_all_records() # this return a list of dictioraies so the key is the name column and the value is the value for that particular column
    
    def write_data(self, range, values): #range ej "A1:V1". values must be a list of list
        self.sheet.update(range, values)

def traer_datos(dias=7):
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

lista_db=(procesamiento_de_datos())

for x in lista_db:
    print(x[0])
    


