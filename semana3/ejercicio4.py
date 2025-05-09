# ALUMNO : LIZA GUERRERO PIERO ALEXANDRO
# CODIGO : 0202114037
# PRACTICA SEMANA 3

import pandas as pd

# 1. Datos del gasto semanal de Ana
gasto_semanal = [4.0, 3.5, 5.0, 4.2, 3.8]

# 2. Crear DataFrame
df = pd.DataFrame(gasto_semanal, columns=['Gasto'])

# 3. Calcular gasto total y medio
gasto_total = df['Gasto'].sum()
gasto_promedio = df['Gasto'].mean()

# 4. Identificar días que gastaron más que el promedio
dias_mayores = df[df['Gasto'] > gasto_promedio]

# 5. Imprimir resultados
print("=== Resultados Ejercicio Gastos de Almuerzo ===")
print(f"Gasto total en la semana: S/ {gasto_total:.2f}")
print(f"Gasto promedio diario: S/ {gasto_promedio:.2f}")
print("Días con gasto superior al promedio:")
for index, row in dias_mayores.iterrows():
    print(f" - Día {index + 1} con gasto S/ {row['Gasto']:.2f}")
