# S08.s1 - Práctica: Representaciones Cromosómicas en Algoritmos Genéticos

## 📚 Descripción

Esta práctica implementa las tres representaciones cromosómicas fundamentales en Algoritmos Genéticos aplicadas a un problema real de distribución equitativa de estudiantes en exámenes.

### Problema a resolver
Un docente tiene 39 alumnos y necesita distribuirlos en 3 exámenes diferentes (A, B, C) con 13 alumnos cada uno. El objetivo es lograr que los grupos sean equilibrados en términos de rendimiento académico.

## 🧬 Representaciones Implementadas

### 1. Representación Binaria (`representacion_binaria.py`)
- **Cromosoma**: 117 bits (39 alumnos × 3 bits cada uno)
- **Codificación**: Cada alumno tiene 3 bits, solo uno activo indicando su examen
- **Ejemplo**: `[0,1,0]` = alumno asignado al examen B
- **Ideal para**: Problemas de selección y asignación discreta

### 2. Representación Real (`representacion_real.py`)
- **Cromosoma**: 117 valores reales (39 alumnos × 3 pesos normalizados)
- **Codificación**: Cada alumno tiene 3 valores que suman 1.0
- **Ejemplo**: `[0.2, 0.5, 0.3]` = probabilidades para A, B, C
- **Ideal para**: Optimización con variables continuas

### 3. Representación Permutacional (`representacion_permutacional.py`)
- **Cromosoma**: Permutación de 39 índices
- **Codificación**: Posiciones [0-12] → A, [13-25] → B, [26-38] → C
- **Ejemplo**: `[34, 25, 32, ...]` = orden de asignación
- **Ideal para**: Problemas de ordenamiento y secuenciación

## 🚀 Instalación y Uso

### Opción 1: Entorno Local
```bash
# Clonar el repositorio
git clone [URL_DEL_REPO]
cd s8_p

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar ejemplos
python representacion_binaria.py
python representacion_real.py
python representacion_permutacional.py
```

### Opción 2: Google Colab
```python
# En una celda de Colab:
!git clone [URL_DEL_REPO]
%cd s8_p
!pip install -r requirements.txt

# Ejecutar los archivos
!python representacion_binaria.py
```

## 📊 Datos de Entrada

El archivo `notas_1u.csv` contiene las notas de los 39 alumnos con su asignación original:
- Columnas: Alumno, Nota, Tipo_Examen
- Notas: Escala de 0 a 20
- Distribución original desequilibrada

## 🎯 Actividades para Estudiantes

### Actividad 1: Análisis Comparativo
1. Ejecuta los tres programas y compara los resultados
2. ¿Cuál representación logra mejor equilibrio entre los grupos?
3. ¿Cuál converge más rápido? (observa las generaciones)
4. Documenta tus observaciones en un archivo `analisis.txt`

### Actividad 2: Modificación de Fitness
1. En `representacion_binaria.py`, modifica la función `calcular_fitness` para:
   - Penalizar grupos con varianza alta de notas
   - Premiar diversidad (mezclar alumnos de diferentes rendimientos)
2. Compara los resultados con la versión original

### Actividad 3: Nuevo Operador Genético
1. En `representacion_real.py`, implementa un operador de mutación diferente:
   ```python
   def mutacion_gaussiana(cromosoma, sigma=0.1):
       # Tu implementación aquí
       # Debe mantener la normalización (suma = 1)
   ```
2. Prueba con diferentes valores de sigma

### Actividad 4: Restricciones Adicionales
1. Modifica `representacion_permutacional.py` para agregar una restricción:
   - Los alumnos con notas < 11 no pueden estar todos en el mismo examen
2. Ajusta la función de fitness para penalizar soluciones que violen esta restricción

### Actividad 5: Visualización (Avanzado)
1. Crea un nuevo archivo `visualizacion.py` que:
   - Grafique la evolución del fitness por generación
   - Muestre un histograma de notas por examen
   - Compare las distribuciones de las 3 representaciones
2. Usa matplotlib o seaborn para las gráficas

### Actividad 6: Problema Extendido
1. Modifica uno de los programas para distribuir los alumnos en 4 exámenes
2. ¿Qué cambios necesitas hacer en el cromosoma?
3. ¿Cómo afecta esto a la convergencia del algoritmo?

## 📝 Entregables

1. **Código modificado**: Sube tus modificaciones a un fork del repositorio
2. **Informe** (2-3 páginas):
   - Comparación de representaciones
   - Resultados de las actividades realizadas
   - Conclusiones sobre cuándo usar cada representación
3. **Extra** (opcional): 
   - Implementa una representación híbrida
   - Propón un problema diferente y resuélvelo con AG

## 🤔 Preguntas de Reflexión

1. ¿Por qué la representación binaria tuvo dificultades para lograr exactamente 13 alumnos por grupo?
2. ¿Qué ventajas tiene usar valores reales normalizados vs. selección directa?
3. ¿En qué casos la representación permutacional sería inadecuada?
4. ¿Cómo afecta el tamaño de la población y número de generaciones a la calidad de la solución?

## 📖 Material de Referencia

- `representaciones_cromosomicas.json`: Teoría completa sobre representaciones
- Documentación de NumPy: https://numpy.org/doc/
- Documentación de Pandas: https://pandas.pydata.org/docs/

## ⚡ Tips de Depuración

- Si el fitness es siempre -1000, revisa las restricciones de tamaño de grupo
- Para debugging, reduce población y generaciones
- Imprime cromosomas intermedios para entender la codificación
- Verifica que las mutaciones mantienen la validez del cromosoma

---
**Autor**: Ms. Ing. Johan Max Alexander López Heredia  
**Curso**: Algoritmos Evolutivos - 1411-2278