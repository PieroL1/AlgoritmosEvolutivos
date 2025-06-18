import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Cargar los datos de los alumnos y sus notas
df = pd.read_csv('Semana8/notas_1u.csv')
alumnos = df['Alumno'].tolist()
notas = df['Nota'].tolist()


# Importar las asignaciones desde los otros archivos
from representacion_binaria import asignaciones_binaria  # Importar desde representacion_binaria.py
from representacion_real import asignaciones_real  # Importar desde representacion_real.py
from representacion_permutacional import asignaciones_permutacional  # Importar desde representacion_permutacional.py
# Asignaciones finales obtenidas de las ejecuciones de los algoritmos
# (Estas asignaciones deben haberse guardado previamente como en los ejemplos anteriores)
asignaciones_binaria = asignaciones_binaria  # Tomadas de representacion_binaria.py
asignaciones_real = asignaciones_real  # Tomadas de representacion_real.py
asignaciones_permutacional = asignaciones_permutacional  # Tomadas de representacion_permutacional.py

# Historial de fitness para las tres representaciones (debe provenir de las ejecuciones previas)
historial_binario = np.random.random(50)  # Reemplazar con el historial real de fitness de la representación binaria
historial_real = np.random.random(50)  # Reemplazar con el historial real de fitness de la representación real
historial_permutacional = np.random.random(50)  # Reemplazar con el historial real de fitness de la representación permutacional

# 1. Graficar la evolución del fitness por generación
plt.figure(figsize=(10, 6))
plt.plot(historial_binario, label='Representación Binaria')
plt.plot(historial_real, label='Representación Real')
plt.plot(historial_permutacional, label='Representación Permutacional')
plt.xlabel('Generación')
plt.ylabel('Fitness')
plt.title('Evolución del Fitness por Generación')
plt.legend()
plt.grid(True)
plt.show()

# 2. Mostrar un histograma de notas por examen
examenes = ['A', 'B', 'C']

# Crear histograma para cada examen (A, B, C)
plt.figure(figsize=(10, 6))
plt.hist([notas[i] for i in asignaciones_binaria['A']], bins=10, alpha=0.5, label='Examen A (Binaria)')
plt.hist([notas[i] for i in asignaciones_binaria['B']], bins=10, alpha=0.5, label='Examen B (Binaria)')
plt.hist([notas[i] for i in asignaciones_binaria['C']], bins=10, alpha=0.5, label='Examen C (Binaria)')

plt.hist([notas[i] for i in asignaciones_real['A']], bins=10, alpha=0.5, label='Examen A (Real)')
plt.hist([notas[i] for i in asignaciones_real['B']], bins=10, alpha=0.5, label='Examen B (Real)')
plt.hist([notas[i] for i in asignaciones_real['C']], bins=10, alpha=0.5, label='Examen C (Real)')

plt.hist([notas[i] for i in asignaciones_permutacional['A']], bins=10, alpha=0.5, label='Examen A (Permutacional)')
plt.hist([notas[i] for i in asignaciones_permutacional['B']], bins=10, alpha=0.5, label='Examen B (Permutacional)')
plt.hist([notas[i] for i in asignaciones_permutacional['C']], bins=10, alpha=0.5, label='Examen C (Permutacional)')

plt.xlabel('Notas')
plt.ylabel('Frecuencia')
plt.title('Distribución de Notas por Examen (para las 3 representaciones)')
plt.legend()
plt.grid(True)
plt.show()

# 3. Comparar las distribuciones de las 3 representaciones
plt.figure(figsize=(10, 6))

# Histograma comparativo
sns.histplot([notas[i] for i in asignaciones_binaria['A']], color='blue', label='Examen A (Binaria)', kde=True, stat="density", linewidth=0)
sns.histplot([notas[i] for i in asignaciones_real['A']], color='green', label='Examen A (Real)', kde=True, stat="density", linewidth=0)
sns.histplot([notas[i] for i in asignaciones_permutacional['A']], color='red', label='Examen A (Permutacional)', kde=True, stat="density", linewidth=0)

plt.xlabel('Notas')
plt.ylabel('Densidad')
plt.title('Comparación de Distribuciones para Examen A (Las 3 Representaciones)')
plt.legend()
plt.grid(True)
plt.show()
