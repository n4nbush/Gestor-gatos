import sqlite3
from datetime import datetime

# --- CONFIGURACIÓN ---
DB_NAME = 'gastos.db'

def add_transaction(transaction_date, type, category_name, amount, description):
    """
    Añade una nueva transacción a la base de datos.
    Esta función se encarga de:
    1. Buscar el ID de la categoría a partir de su nombre.
    2. Insertar la transacción en la tabla 'transactions' con el ID correcto.
    """
    conn = None # Definimos conn como None al principio
    try:
        # --- Conexión a la DB ---
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        # --- Lógica Principal (El Corazón del Proceso) ---

        # 1. Buscar el ID de la categoría
        # A partir del nombre de la categoría (ej: "Moto"), obtenemos su ID.
        print(f"Buscando el ID para la categoría: '{category_name}'...")
        cursor.execute("SELECT id FROM categorias WHERE name = ?", (category_name,))
        resultado = cursor.fetchone()

        # 2. Validar si la categoría existe
        if resultado is None:
            print(f"❌ ERROR: La categoría '{category_name}' no existe en la base de datos.")
            print("Por favor, añádela primero a la tabla 'categorias'.")
            return False # Devolvemos False para indicar que la operación falló
        
        category_id = resultado[0]
        print(f"✅ ID encontrado: {category_id}")

        # 3. Limpiar y preparar los datos
        # (Por ahora, asumimos que los datos vienen limpios, pero aquí iría la lógica)
        # Por ejemplo, convertir la fecha a un string en formato ISO
        formatted_date = transaction_date.isoformat()

        # 4. Insertar la transacción en la tabla 'transactions'
        print(f"Insertando transacción en la base de datos...")
        sql_insert = """
        INSERT INTO transactions (transaction_date, type, amount, description, category_id)
        VALUES (?, ?, ?, ?, ?);
        """
        cursor.execute(sql_insert, (formatted_date, type, amount, description, category_id))
        
        # 5. Guardar los cambios
        conn.commit()
        
        print(f"✅ ¡Transacción guardada con éxito! (ID: {cursor.lastrowid})")
        return True # Devolvemos True para indicar éxito

    except sqlite3.Error as e:
        print(f"❌ Ocurrió un error de base de datos: {e}")
        if conn:
            conn.rollback() # Revertimos los cambios si hubo un error
        return False
        
    finally:
        if conn:
            conn.close()
            print("Conexión cerrada.")

# --- PRUEBA DE LA FUNCIÓN ---
if __name__ == "__main__":
    print("--- Probando la función add_transaction ---")

    # Prueba 1: Un gasto válido
    print("\n--- [Prueba 1: Gasto válido] ---")
    add_transaction(
        transaction_date=datetime.now(),
        type="Gasto",
        category_name="Moto", # Usa una categoría que sepas que existe
        amount=-7500.50,
        description="Nafta súper"
    )

    # Prueba 2: Un ingreso válido
    print("\n--- [Prueba 2: Ingreso válido] ---")
    add_transaction(
        transaction_date=datetime(2025, 11, 10), # Una fecha específica
        type="Ingreso",
        category_name="Salario", # Asegúrate de que "Salario" exista como categoría
        amount=500000,
        description="Primera quincena"
    )

    # Prueba 3: Una categoría que NO existe
    print("\n--- [Prueba 3: Categoría inválida] ---")
    add_transaction(
        transaction_date=datetime.now(),
        type="Gasto",
        category_name="Cohete Espacial", # Esta categoría no debería existir
        amount=-1000000,
        description="Viaje a Marte"
    )