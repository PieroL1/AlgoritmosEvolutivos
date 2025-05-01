import pandas as pd

costo_hora_pc = 2

# Construimos el diccionario de datos estudiante y horas usadas
datos = {
    'Estudiante': ['Ana', 'Luis', 'María', 'Juan', 'Carla'],
    'Horas_usadas': [3, 5, 2, 4, 1]
}

# Creamos un dataframe con los datos anteriores
df = pd.DataFrame(datos)

# Añadimos la columna 'Costo_total' multiplicando las horas por 2.0 (costo por hora)
df['Costo_total'] = df['Horas_usadas'] * 2.0

# Mostramos el DataFrame con .head() para ver cómo quedó
print('TABLA DE DATOS')
print(df.head())

# Estadísticas descriptivas de la columna 'Costo_total'
print(df['Costo_total'].describe())


# Filtrar estudiantes que han gastado más de S/ 6.00
gasto_mayor_6 = df[df['Costo_total'] > 6.0]

# Mostrar los resultados
print(gasto_mayor_6)

# Calcular el gasto promedio
gasto_promedio = df['Costo_total'].mean()

# Obtener la lista de estudiantes que han gastado más de S/ 6.00
estudiantes_mayor_6 = gasto_mayor_6['Estudiante'].tolist()

# Imprimir el resumen
print(f"El gasto promedio fue de S/{gasto_promedio:.2f}; los estudiantes que gastaron más de S/6.00 son: {estudiantes_mayor_6}.")
