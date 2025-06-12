import pandas as pd
import numpy as np
import random

# Cargar matriz de distancias
file_path_3 = 'Semana5\ejercicio3.xlsx'
df_dist = pd.read_excel(file_path_3, index_col=0)

# Lista de laboratorios
labs = df_dist.index.tolist()
num_labs = len(labs)

def calcular_distancia_total(ruta, matriz_dist):
    """
    Calcula la distancia total de la ruta, incluyendo regreso al inicio.
    """
    distancia = 0
    for i in range(len(ruta)-1):
        distancia += matriz_dist.loc[ruta[i], ruta[i+1]]
    # Regresar al punto de inicio
    distancia += matriz_dist.loc[ruta[-1], ruta[0]]
    return distancia

def generar_solucion_inicial(labs):
    """
    Genera una ruta inicial aleatoria.
    """
    ruta = labs.copy()
    random.shuffle(ruta)
    return ruta

def generar_vecindad(ruta):
    """
    Genera vecinos intercambiando dos laboratorios en la ruta.
    """
    vecinos = []
    for i in range(len(ruta)):
        for j in range(i+1, len(ruta)):
            vecino = ruta.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)
    return vecinos

def hill_climbing_tsp(df_dist, labs, max_iter=1000):
    """
    Algoritmo hill climbing para TSP.
    """
    current_solution = generar_solucion_inicial(labs)
    current_cost = calcular_distancia_total(current_solution, df_dist)
    
    for _ in range(max_iter):
        vecinos = generar_vecindad(current_solution)
        mejor_vecino = None
        mejor_costo = current_cost
        
        for vecino in vecinos:
            costo_vecino = calcular_distancia_total(vecino, df_dist)
            if costo_vecino < mejor_costo:
                mejor_costo = costo_vecino
                mejor_vecino = vecino
        
        if mejor_costo < current_cost:
            current_solution = mejor_vecino
            current_cost = mejor_costo
        else:
            break  # No hay mejora, termina
    
    return current_solution, current_cost

# Ejecutar hill climbing
ruta_optima, distancia_optima = hill_climbing_tsp(df_dist, labs)

print(f"Ruta óptima encontrada (orden de visita): {ruta_optima}")
print(f"Distancia total mínima aproximada: {distancia_optima:.2f} metros")
