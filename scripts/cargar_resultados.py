import psycopg2
from psycopg2.extras import execute_values
import sys

ruta_archivo = "part-00000"

print(f"Abriendo {ruta_archivo}...")

try:
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="datamart_db",
        user="datamart_admin",
        password="super_secreto_123"
    )
    cur = conn.cursor()

    # Limpiar la tabla por si quedaron inserciones parciales
    cur.execute("TRUNCATE TABLE resultados_ingresos;")
    conn.commit()

    with open(ruta_archivo, "r") as f:
        registros = []
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 3:
                registros.append((parts[0], parts[1], float(parts[2])))

    print(f"Leídos {len(registros)} registros. Insertando masivamente en PostgreSQL...")

    # Inserción ultrarrápida masiva
    query = "INSERT INTO resultados_ingresos (hora, categoria, ingreso_total) VALUES %s"
    execute_values(cur, query, registros, page_size=10000)

    conn.commit()
    cur.close()
    conn.close()

    print(f"¡Éxito total! Se cargaron {len(registros)} registros a PostgreSQL correctamente.")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo {ruta_archivo} en la carpeta scripts.")
except Exception as e:
    print(f"Error en la base de datos: {e}")