# ALUMNO : LIZA GUERRERO PIERO ALEXANDRO
# CODIGO : 0202114037
# PRACTICA SEMANA 3

import numpy as np

# 1. Presupuesto disponible
presupuesto = 15.0

# 2. Precios de los pasajes de bus, combi y tren
precios_transporte = np.array([2.50, 3.00, 1.80])

# 3. Determinar cuántos viajes puede pagar con cada medio
max_viajes = np.floor(presupuesto / precios_transporte)

# 4. Encontrar el medio de transporte que le permite más viajes
indice_max = int(max_viajes.argmax())

# 5. Imprimir resultados
transportes = ['Bus', 'Combi', 'Tren']
print("=== Resultados Ejercicio Viajes ===")
for i, transporte in enumerate(transportes):
    print(f"{transporte}: precio S/ {precios_transporte[i]:.2f} → puede hacer {int(max_viajes[i])} viajes")

print(f"\nCon S/ {presupuesto:.2f} puede hacer más viajes en {transportes[indice_max]} con {int(max_viajes[indice_max])} viajes.")
