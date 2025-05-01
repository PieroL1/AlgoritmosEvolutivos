
# Se importa la libreria que se va a usar
import numpy as np
# Creamos la variable con nuestro presupuesto
presupuesto = 10
# Creamos un array con los precios de los cafes y hacemos con numpy
precios_cafe = np.array([2.50, 3.00, 1.75, 2.20])
# Aqui vamos a dar a max_cafes el valor del presupuesto sobre cada precio y lo guarda en array
max_cafes = np.floor(presupuesto / precios_cafe)
# Imprimimos ma_cafes para ver los resultados
print(max_cafes)

# Usamos max() para obtener el valor máximo (mayor cantidad de cafés)
cantidad_maxima = max_cafes.max()
# Usamos argmax() para obtener la posición de la cantidad máxima
posicion_maxima = max_cafes.argmax()

print("La mayor cantidad de cafés vendidos es:", cantidad_maxima)
print("La posición donde se vendió la mayor cantidad de cafés es:", posicion_maxima)

# Colocamos el nombre de la cafeteria en el mismo orden de precios
nombres_cafe = ['A', 'B', 'C', 'D']



# Imprimimos el mensaje con el resultado final
print(f"Con S/{presupuesto} puedo comprar como máximo {cantidad_maxima} cafés en la cafetería {nombres_cafe[posicion_maxima]} (precio mínimo S/{precios_cafe[posicion_maxima]:.2f}).")