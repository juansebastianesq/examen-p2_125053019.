#!/usr/bin/env python3
import sys

current_key = None
current_total = 0.0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.split("\t")
    if len(parts) != 3:
        continue
    
    hora, categoria, ingreso_str = parts
    try:
        ingreso = float(ingreso_str)
    except ValueError:
        continue
    
    key = f"{hora}\t{categoria}"
    
    if current_key == key:
        current_total += ingreso
    else:
        if current_key:
            prev_hora, prev_cat = current_key.split("\t")
            print(f"{prev_hora}\t{prev_cat}\t{round(current_total, 2)}")
        current_key = key
        current_total = ingreso

# Imprimir la última clave procesada
if current_key:
    prev_hora, prev_cat = current_key.split("\t")
    print(f"{prev_hora}\t{prev_cat}\t{round(current_total, 2)}")