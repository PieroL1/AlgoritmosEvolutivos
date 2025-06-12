import pandas as pd

# Cargar archivo Excel con las notas
file_path = 'Semana5\\Grades.xlsx'  # Mejor usar doble barra invertida o raw string para evitar warnings
df = pd.read_excel(file_path)

def fitness(offset, df):
    """
    Calcula la función de aptitud para un offset dado.

    Parámetros:
    - offset: número flotante, el valor que se suma a cada nota.
    - df: DataFrame con las notas originales.

    Retorna:
    - Porcentaje de alumnos aprobados (promedio ≥ 7) si promedio clase ≤ 14.
    - -1 si el promedio de la clase supera 14 (penalización).
    """
    # Aplicar offset a los tres parciales
    adjusted_scores = df[['Parcial1', 'Parcial2', 'Parcial3']] + offset
    
    # Calcular promedio por alumno
    student_means = adjusted_scores.mean(axis=1)
    
    # Calcular porcentaje de aprobados
    approved_percentage = (student_means >= 7).mean() * 100
    
    # Calcular promedio general de la clase
    class_mean = student_means.mean()
    
    # Penalización si promedio > 14
    if class_mean > 14:
        return -1
    
    return approved_percentage

def hill_climbing(df, step=0.5, offset_min=-5, offset_max=5):
    """
    Aplica el algoritmo hill climbing para encontrar el offset óptimo.

    Parámetros:
    - df: DataFrame con notas originales.
    - step: tamaño del paso para el offset.
    - offset_min, offset_max: rango donde buscar el offset.

    Retorna:
    - offset_optimo: el valor del offset que maximiza la aptitud.
    - best_fitness: valor máximo de la aptitud.
    """
    current_offset = 0
    current_fitness = fitness(current_offset, df)
    improving = True
    
    while improving:
        improving = False
        # Generar vecinos posibles (offset +- step, dentro del rango)
        neighbors = []
        if current_offset - step >= offset_min:
            neighbors.append(current_offset - step)
        if current_offset + step <= offset_max:
            neighbors.append(current_offset + step)
        
        for neighbor in neighbors:
            fit = fitness(neighbor, df)
            if fit > current_fitness:
                current_offset = neighbor
                current_fitness = fit
                improving = True
                break  # Tomamos la primera mejora que encontremos
    
    return current_offset, current_fitness

# Ejecutar hill climbing
offset_optimo, max_aptitud = hill_climbing(df)

# Mostrar resultados
print(f"Offset óptimo encontrado: {offset_optimo}")
print(f"Porcentaje máximo de aprobados con restricción: {max_aptitud:.2f}%")

# Aplicar offset óptimo para ver distribución final
df_adjusted = df.copy()
df_adjusted[['Parcial1', 'Parcial2', 'Parcial3']] += offset_optimo
df_adjusted['Promedio'] = df_adjusted[['Parcial1', 'Parcial2', 'Parcial3']].mean(axis=1)

# Calcular promedio general final
promedio_general_final = df_adjusted['Promedio'].mean()
print(f"Promedio general final de la clase: {promedio_general_final:.2f}")

print("\nDistribución final de notas (primeros 10 alumnos):")
print(df_adjusted.head(10))
