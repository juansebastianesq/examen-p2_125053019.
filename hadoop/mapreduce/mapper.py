#!/usr/bin/env python3
import sys

# Formato del CSV:
# id, fecha_hora, tienda, categoria, producto, cantidad, precio_unitario, metodo_pago

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    # Manejar/ignorar la línea de encabezado
    if line.startswith("id,") or line.startswith("id\t"):
        continue
    
    fields = line.split(",")
    if len(fields) != 8:
        continue  # Manejo de líneas mal formadas sin truncar el job
    
    try:
        fecha_hora = fields[1].strip()
        categoria = fields[3].strip()
        cantidad = float(fields[5])
        precio_unitario = float(fields[6])
        
        # Extraer únicamente la hora (00 - 23) de 'YYYY-MM-DD HH:MM:SS'
        hora = fecha_hora.split(" ")[1].split(":")[0]
        
        # Calcular el ingreso total de la transacción
        ingreso = cantidad * precio_unitario
        
        # Clave: Hora\tCategoria  Valor: Ingreso
        print(f"{hora}\t{categoria}\t{ingreso}")
    except (ValueError, IndexError):
        # Ignorar registros corruptos o con mal formato
        continue