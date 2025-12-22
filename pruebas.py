import sqlite3

conn = sqlite3.connect('gastos.db')

cursor = conn.cursor()

cursor.execute("""

    SELECT * FROM datos
    WHERE FECHA >= date ('now')
    order by FECHA DESC

               
""")

resultados = cursor.fetchall()

print (resultados)