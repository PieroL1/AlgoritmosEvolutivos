import pandas as pd
import random

# Cargar datos
file_path_6 = 'Semana5\ejercicio6.xlsx'
df = pd.read_excel(file_path_6)

max_time = 90
min_difficulty = 180
max_difficulty = 200

def fitness(solucion, df):
    total_time = 0
    total_diff = 0
    for i, bit in enumerate(solucion):
        if bit == 1:
            total_time += df.loc[i, 'Time_min']
            total_diff += df.loc[i, 'Difficulty']
    
    # Penalización por tiempo excedido (gran penalización)
    if total_time > max_time:
        return -1000 * (total_time - max_time)
    
    # Penalización proporcional si dificultad fuera del rango
    if total_diff < min_difficulty:
        return total_diff - 10 * (min_difficulty - total_diff)
    if total_diff > max_difficulty:
        return max_difficulty - 10 * (total_diff - max_difficulty)
    
    # Dentro del rango, recompensa por dificultad total
    return total_diff

def generar_solucion_inicial(n):
    return [random.choice([0,1]) for _ in range(n)]

def vecindad(solucion):
    vecinos = []
    for i in range(len(solucion)):
        vecino = solucion.copy()
        vecino[i] = 1 - vecino[i]  # Cambiar inclusión/exclusión
        vecinos.append(vecino)
    return vecinos

def hill_climbing(df, max_iter=1000):
    n = len(df)
    current_solution = generar_solucion_inicial(n)
    current_fitness = fitness(current_solution, df)
    
    for _ in range(max_iter):
        vecinos = vecindad(current_solution)
        mejor_vecino = None
        mejor_fitness = current_fitness
        
        for vecino in vecinos:
            fit = fitness(vecino, df)
            if fit > mejor_fitness:
                mejor_fitness = fit
                mejor_vecino = vecino
                
        if mejor_vecino is not None:
            current_solution = mejor_vecino
            current_fitness = mejor_fitness
        else:
            break  # No mejora
    
    return current_solution, current_fitness

# Ejecutar hill climbing
solucion_optima, mejor_fitness = hill_climbing(df)

# Mostrar resultados
preguntas_seleccionadas = [df.loc[i, 'QuestionID'] for i, bit in enumerate(solucion_optima) if bit == 1]
tiempo_total = sum(df.loc[i, 'Time_min'] for i, bit in enumerate(solucion_optima) if bit == 1)
dificultad_total = sum(df.loc[i, 'Difficulty'] for i, bit in enumerate(solucion_optima) if bit == 1)

print(f"Dificultad total del examen: {dificultad_total}")
print(f"Tiempo total estimado: {tiempo_total} minutos")
print(f"Preguntas seleccionadas ({len(preguntas_seleccionadas)}): {preguntas_seleccionadas}")
