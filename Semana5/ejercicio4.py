import pandas as pd
import random
import numpy as np

file_path_4 = r'Semana5\ejercicio4.xlsx'
df = pd.read_excel(file_path_4)

presupuesto_max = 10000

def fitness(solucion, df, presupuesto_max):
    total_costo = 0
    total_beneficio = 0
    for i, incluido in enumerate(solucion):
        if incluido:
            total_costo += df.loc[i, 'Cost_Soles']
            total_beneficio += df.loc[i, 'Benefit_Soles']
    if total_costo > presupuesto_max:
        return 0
    return total_beneficio

def generar_solucion_inicial(n):
    return [random.choice([0,1]) for _ in range(n)]

def vecindad(solucion):
    vecinos = []
    for i in range(len(solucion)):
        vecino = solucion.copy()
        vecino[i] = 1 - vecino[i]
        vecinos.append(vecino)
    return vecinos

def hill_climbing(df, presupuesto_max, iteraciones=1000):
    n = len(df)
    current_solution = generar_solucion_inicial(n)
    current_fitness = fitness(current_solution, df, presupuesto_max)

    for _ in range(iteraciones):
        vecinos = vecindad(current_solution)
        mejor_vecino = None
        mejor_fitness = current_fitness

        for vecino in vecinos:
            fit = fitness(vecino, df, presupuesto_max)
            if fit > mejor_fitness:
                mejor_fitness = fit
                mejor_vecino = vecino
        
        if mejor_fitness > current_fitness:
            current_solution = mejor_vecino
            current_fitness = mejor_fitness
        else:
            break
    
    return current_solution, current_fitness

solucion_optima, beneficio_max = hill_climbing(df, presupuesto_max)

import numpy as np
mascara = np.array(solucion_optima, dtype=bool)
proyectos_seleccionados = df[mascara]

print(f"Beneficio máximo con presupuesto S/ {presupuesto_max}: {beneficio_max}")
print("\nProyectos seleccionados:")
print(proyectos_seleccionados)
