# ALUMNO : LIZA GUERRERO PIERO ALEXANDRO
# CODIGO : 0202114037
# PRACTICA SEMANA 3

import numpy as np

# 1. Definimos los datos de paquetes y precios
paquetes = np.array([1, 2, 5, 10])   # en GB
precios = np.array([5, 9, 20, 35])   # en soles

# 2. Calculamos el costo por GB dividiendo precio entre GB
costo_por_gb = precios / paquetes

# 3. Buscamos el valor mínimo y el índice correspondiente
costo_min = costo_por_gb.min()
indice_min = costo_por_gb.argmin()

# 4. Imprimir resultados
print("=== Resultados Ejercicio Datos Móviles ===")
for i in range(len(paquetes)):
    print(f"Paquete de {paquetes[i]}GB → S/ {precios[i]} → Costo por GB: S/ {costo_por_gb[i]:.2f}")

print(f"\nEl paquete más económico por GB es el de {paquetes[indice_min]}GB con un costo de S/ {costo_min:.2f} por GB.")
