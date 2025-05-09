# ALUMNO : LIZA GUERRERO PIERO ALEXANDRO
# CODIGO : 0202114037
# PRACTICA SEMANA 3

import numpy as np

# 1. Presupuesto disponible
presupuesto = 8.0

# 2. Precios por página en cada copistería
precios = np.array([0.10, 0.12, 0.08])

# 3. Cuántas páginas puede fotocopiar en cada copistería
max_paginas = np.floor(presupuesto / precios)

# 4. Encontrar la copistería que le permite fotocopiar más páginas
indice_max = int(max_paginas.argmax())  # Índice de la copistería con más páginas

# 5. Imprimir resultados
copisterias = ['Copistería 1', 'Copistería 2', 'Copistería 3']
print("=== Resultados Ejercicio Fotocopias ===")
for i, nombre in enumerate(copisterias):
    print(f"{nombre}: precio S/ {precios[i]:.2f} → puede fotocopiar {int(max_paginas[i])} páginas")

print(f"\nCon S/ {presupuesto:.2f} obtiene más páginas en {copisterias[indice_max]}siendo, {int(max_paginas[indice_max])} páginas.")
