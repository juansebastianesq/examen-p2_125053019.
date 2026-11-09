from fastapi import FastAPI, HTTPException
import psycopg2
import os
from pydantic import BaseModel

app = FastAPI()

# Configuración de la conexión a PostgreSQL (usa el nombre del servicio 'db' en docker-compose)
def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database=os.environ.get("POSTGRES_DB", "datamart_db"),
        user=os.environ.get("POSTGRES_USER", "datamart_admin"),
        password=os.environ.get("POSTGRES_PASSWORD", "super_secreto_123")
    )
    return conn

# Modelo para escribir datos
class IngresoData(BaseModel):
    hora: str
    categoria: str
    ingreso_total: float

@app.on_event("startup")
def startup():
    # Crear la tabla si no existe cuando arranca la API
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS resultados_ingresos (
            id SERIAL PRIMARY KEY,
            hora VARCHAR(2),
            categoria VARCHAR(50),
            ingreso_total NUMERIC(15, 2)
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# GET: Todos los registros
@app.get("/ingresos")
def obtener_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT hora, categoria, ingreso_total FROM resultados_ingresos;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"hora": r[0], "categoria": r[1], "ingreso_total": float(r[2])} for r in rows]

# GET: Filtro por categoría (Clave de tu pregunta)
@app.get("/ingresos/{categoria}")
def obtener_por_categoria(categoria: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT hora, categoria, ingreso_total FROM resultados_ingresos WHERE categoria = %s;", (categoria,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"hora": r[0], "categoria": r[1], "ingreso_total": float(r[2])} for r in rows]

# POST: Insertar un nuevo registro (CRUD original sobre la nueva tabla)
@app.post("/ingresos")
def crear_ingreso(data: IngresoData):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO resultados_ingresos (hora, categoria, ingreso_total) VALUES (%s, %s, %s)",
        (data.hora, data.categoria, data.ingreso_total)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"mensaje": "Registro insertado exitosamente"}