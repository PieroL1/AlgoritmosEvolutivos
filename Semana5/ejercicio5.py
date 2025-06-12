import pandas as pd
import numpy as np
import random

# Cargar datos
file_path_5 = 'Semana5\ejercicio5.xlsx'
df = pd.read_excel(file_path_5)

tesistas = df['TesistaID'].tolist()
franjas = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']
salas = [f'Sala{i+1}' for i in range(6)]

num_tesistas = len(tesistas)
num_salas = len(salas)
num_franjas = len(franjas)

# Representar solución como lista de tuplas: (sala, franja) para cada tesista
# Heurística inicial: asignación secuencial por franjas y salas
def asignacion_inicial():
    asignacion = []
    idx_sala = 0
    idx_franja = 0
    for i in range(num_tesistas):
        # Buscar próxima franja disponible para el tesista i
        while df.loc[i, franjas[idx_franja]] == 0:
            idx_franja += 1
            if idx_franja == num_franjas:
                idx_franja = 0
                idx_sala = (idx_sala + 1) % num_salas
        asignacion.append( (salas[idx_sala], franjas[idx_franja]) )
        idx_franja += 1
        if idx_franja == num_franjas:
            idx_franja = 0
            idx_sala = (idx_sala + 1) % num_salas
    return asignacion

# Función para calcular solapamientos
def contar_solapamientos(asignacion):
    # Contar cuántos tesistas están asignados a la misma (sala, franja)
    conteo = {}
    solapamientos = 0
    for s in asignacion:
        conteo[s] = conteo.get(s, 0) + 1
    for v in conteo.values():
        if v > 1:
            solapamientos += v - 1
    return solapamientos

# Función para calcular huecos y uso continuo > 4 horas
def calcular_huecos_y_continuo(asignacion):
    # Para cada sala, obtener franjas asignadas (convertir F1..F6 a índices 0..5)
    huecos_totales = 0
    penalizacion_continuo = 0
    
    franjas_idx = {f: i for i, f in enumerate(franjas)}
    
    for sala in salas:
        franjas_asignadas = [franjas_idx[fr] for (sal, fr) in asignacion if sal == sala]
        franjas_asignadas = sorted(franjas_asignadas)
        if not franjas_asignadas:
            continue
        # Contar huecos (intervalos vacíos entre franjas asignadas)
        for i in range(len(franjas_asignadas) - 1):
            huecos = franjas_asignadas[i+1] - franjas_asignadas[i] - 1
            huecos_totales += huecos
        
        # Verificar si hay uso continuo > 4 franjas (horas)
        # Buscamos la máxima secuencia consecutiva en franjas_asignadas
        max_consecutivo = 1
        contador = 1
        for i in range(1, len(franjas_asignadas)):
            if franjas_asignadas[i] == franjas_asignadas[i-1] + 1:
                contador += 1
                max_consecutivo = max(max_consecutivo, contador)
            else:
                contador = 1
        if max_consecutivo > 4:
            penalizacion_continuo += max_consecutivo - 4
    
    return huecos_totales, penalizacion_continuo

# Vecindad: mover un tesista a otra sala o franja disponible
def generar_vecindad(asignacion):
    vecinos = []
    for i in range(num_tesistas):
        sala_actual, franja_actual = asignacion[i]
        for sala_nueva in salas:
            for franja_nueva in franjas:
                if (sala_nueva, franja_nueva) != (sala_actual, franja_actual):
                    # Solo asignar si tesista está disponible en esa franja
                    if df.loc[i, franja_nueva] == 1:
                        vecino = asignacion.copy()
                        vecino[i] = (sala_nueva, franja_nueva)
                        vecinos.append(vecino)
    return vecinos

# Función objetivo: minimizar solapamientos + huecos + penalizaciones
def funcion_costo(asignacion):
    solap = contar_solapamientos(asignacion)
    huecos, penal_cont = calcular_huecos_y_continuo(asignacion)
    # Ponderamos penalizaciones (puedes ajustar pesos)
    costo = solap * 10 + huecos * 1 + penal_cont * 20
    return costo

# Algoritmo hill climbing
def hill_climbing():
    actual = asignacion_inicial()
    costo_actual = funcion_costo(actual)
    mejor = actual
    mejor_costo = costo_actual
    iteraciones = 0
    
    while iteraciones < 1000:
        vecinos = generar_vecindad(actual)
        mejora = False
        for vecino in vecinos:
            costo_vecino = funcion_costo(vecino)
            if costo_vecino < costo_actual:
                actual = vecino
                costo_actual = costo_vecino
                mejora = True
                if costo_actual < mejor_costo:
                    mejor = actual
                    mejor_costo = costo_actual
                break
        if not mejora:
            break
        iteraciones += 1
    return mejor, mejor_costo

# Ejecutar
solucion_final, costo_final = hill_climbing()

# Reportar resultados
print(f"Costo final (menor es mejor): {costo_final}")

# Crear DataFrame para mostrar calendario final
calendario = pd.DataFrame(columns=['TesistaID', 'Sala', 'Franja'])
for i, asign in enumerate(solucion_final):
    calendario = pd.concat([calendario, pd.DataFrame({
        'TesistaID': [tesistas[i]],
        'Sala': [asign[0]],
        'Franja': [asign[1]]
    })], ignore_index=True)

print("\nCalendario final de defensas:")
print(calendario.sort_values(by=['Sala', 'Franja']).reset_index(drop=True))
