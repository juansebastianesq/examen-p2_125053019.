import time
import csv
import sys

# Iniciar medición de tiempo
start_time = time.time()
resultados = {}

# Ruta del dataset (asume que se ejecuta dentro del contenedor donde se monta el volumen)
dataset_path = "/dataset/ventas.csv"

print("Iniciando procesamiento secuencial...")

try:
    with open(dataset_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Ignorar encabezado
        
        for row in reader:
            if len(row) != 8:
                continue
            
            try:
                fecha_hora = row[1].strip()
                categoria = row[3].strip()
                cantidad = float(row[5])
                precio_unitario = float(row[6])
                
                # Extraer la hora
                hora = fecha_hora.split(" ")[1].split(":")[0]
                ingreso = cantidad * precio_unitario
                
                key = f"{hora}\t{categoria}"
                if key in resultados:
                    resultados[key] += ingreso
                else:
                    resultados[key] = ingreso
            except (ValueError, IndexError):
                continue
                
except FileNotFoundError:
    print(f"Error: No se encontró el archivo en {dataset_path}. Asegúrate de ejecutarlo dentro del contenedor Docker.")
    sys.exit(1)

# Calcular tiempo final
end_time = time.time()

# Mostrar un par de resultados como prueba y el tiempo total
print("\nMuestra de resultados:")
count = 0
for k, v in sorted(resultados.items()):
    if count < 5:
        print(f"{k}\t{round(v, 2)}")
        count += 1

print(f"\nTiempo de ejecución secuencial: {round(end_time - start_time, 2)} segundos")