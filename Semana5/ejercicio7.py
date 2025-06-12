import pandas as pd
import numpy as np
import random
from collections import Counter

# Cargar datos
file_path_7 = 'Semana5\ejercicio7.xlsx'
df = pd.read_excel(file_path_7)

num_teams = 5
team_size = 4
num_students = len(df)

# Obtener lista de habilidades únicas para distribución ideal
skills = df['Skill'].unique()
ideal_skill_dist = {skill: team_size / len(skills) for skill in skills}  # ideal uniforme

# Solución: lista de listas, cada una con índices de alumnos en el equipo
def generar_solucion_inicial():
    indices = list(range(num_students))
    random.shuffle(indices)
    equipos = [indices[i*team_size:(i+1)*team_size] for i in range(num_teams)]
    return equipos

def calcular_varianza_gpa(equipos):
    promedios = []
    for equipo in equipos:
        gpas = df.loc[equipo, 'GPA']
        promedios.append(gpas.mean())
    return np.var(promedios)

def penalizacion_habilidades(equipos):
    penalizacion = 0
    for equipo in equipos:
        skill_counts = Counter(df.loc[equipo, 'Skill'])
        for skill in skills:
            penalizacion += abs(skill_counts.get(skill,0) - ideal_skill_dist[skill])
    return penalizacion

def funcion_aptitud(equipos):
    varianza = calcular_varianza_gpa(equipos)
    penal_habs = penalizacion_habilidades(equipos)
    return varianza + penal_habs  # queremos minimizar

def generar_vecindad(equipos):
    vecinos = []
    for i in range(num_teams):
        for j in range(i+1, num_teams):
            for idx_i, alumno_i in enumerate(equipos[i]):
                for idx_j, alumno_j in enumerate(equipos[j]):
                    vecino = [eq.copy() for eq in equipos]
                    vecino[i][idx_i], vecino[j][idx_j] = vecino[j][idx_j], vecino[i][idx_i]
                    vecinos.append(vecino)
    return vecinos

def hill_climbing(max_iter=1000):
    current_solution = generar_solucion_inicial()
    current_apt = funcion_aptitud(current_solution)
    
    for _ in range(max_iter):
        vecinos = generar_vecindad(current_solution)
        mejor_vecino = None
        mejor_apt = current_apt
        
        for vecino in vecinos:
            apt = funcion_aptitud(vecino)
            if apt < mejor_apt:
                mejor_apt = apt
                mejor_vecino = vecino
                
        if mejor_vecino is not None:
            current_solution = mejor_vecino
            current_apt = mejor_apt
        else:
            break
    
    return current_solution, current_apt

# Ejecutar hill climbing
equipos_optimos, aptitud_optima = hill_climbing()

# Mostrar resultados
print(f"Aptitud (varianza GPA + penalización habilidades): {aptitud_optima:.4f}")

for i, equipo in enumerate(equipos_optimos):
    print(f"\nEquipo {i+1}:")
    print(df.loc[equipo][['StudentID', 'GPA', 'Skill']])
