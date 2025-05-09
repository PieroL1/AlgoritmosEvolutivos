# ALUMNO : LIZA GUERRERO PIERO ALEXANDRO
# CODIGO : 0202114037
# PRACTICA SEMANA 3

import pandas as pd

# 1. Datos de los estudiantes y sus días de préstamo
datos = {
    'Estudiante': ['Rosa', 'David', 'Elena', 'Mario', 'Paula'],
    'Días_prestamo': [7, 10, 5, 12, 3]
}

# 2. Crear DataFrame
df = pd.DataFrame(datos)

# 3. Calcular estadísticas descriptivas de los días de préstamo
estadisticas = df['Días_prestamo'].describe()

# 4. Filtrar estudiantes que retuvieron el libro más de 8 días
df_mayor_8 = df[df['Días_prestamo'] > 8]

# 5. Imprimir resultados
promedio = estadisticas['mean']
max_dias = estadisticas['max']
print("=== Resultados Ejercicio Préstamo de Libros ===")
print(f"Gasto promedio en días de préstamo: {promedio:.2f} días.")
print(f"Estudiantes que retuvieron el libro más de 8 días:")
for alumno in df_mayor_8['Estudiante']:
    print(f" - {alumno}")
