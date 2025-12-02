import sqlite3

conn = sqlite3.connect('gastos.db')

cursor = conn.cursor()




sql_create_groups_table = """
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        group_id INTEGER NOT NULL,
        FOREIGN KEY (group_id) REFERENCES groups (id)
    );
"""
#cursor.execute(sql_create_groups_table)

sql_borrar_tabla = """
    DROP TABLE IF EXISTS categorias;
"""
#cursor.execute(sql_borrar_tabla)

sql_update = """
UPDATE categorias
SET group_id = 7
WHERE id = 27;
"""
#cursor.execute(sql_update)


categorias = {"Internet","Luz","Celular","Ferretería","Servicios Digitales","Moto","SUBE","Uber","Clio","Deuda Viejo","Tarjeta Master","Tarjeta Visa","Deuda Banco","Almacén","Comida Trabajo","Gastos Hormiga","Agustina","Boris","Niñera","Ropa","Psicóloga","Gustos","Peluquería","Farmacia","GIM","Indoor",'Salario','Inversiones','Regalo','Reembolso','Otros ingresos'}

grupos = {"🏠 Hogar y Servicios","🚗 Transporte y Movilidad","🧾 Finanzas y Deudas","🛒 Consumo y Vida Diaria","👨‍👩‍👦 Familia","🧍‍♂️ Bienestar y Personales"
}


def añadir(group_id):
    for x in categorias:
        nombre_categoria = x
        try:
            cursor.execute("INSERT INTO categorias (name,group_id) VALUES (?,?)", (nombre_categoria,group_id))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"El grupo '{nombre_categoria}' ya existe.")
       
#añadir()

sql_query = """
SELECT g.name 
FROM categorias AS c
JOIN grupos AS g ON c.group_id = g.id
WHERE c.name = ?
"""
def chequeo():
    for x in categorias:
        cursor.execute(sql_query, (x,))

        # .fetchone() obtiene la primera (y en este caso, única) fila del resultado
        resultado = cursor.fetchone()

        if resultado:
            nombre_del_grupo = resultado[0]
            print(f"La categoría '{x}' pertenece al grupo: '{nombre_del_grupo}'")
        else:
            print(f"No se encontró la categoría '{x}'")


chequeo()

conn.commit()

conn.close()