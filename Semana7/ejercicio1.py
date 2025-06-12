import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de estilo
sns.set_style("darkgrid")
plt.rcParams.update({
    'axes.titlesize': 16,         # Tamaño del título del gráfico
    'axes.labelsize': 14,         # Tamaño de los textos de los ejes X e Y
    'xtick.labelsize': 12,        # Tamaño de los números en el eje X
    'ytick.labelsize': 12,        # Tamaño de los números en el eje Y
    'figure.figsize': (10, 6)     # Tamaño estándar de todos los gráficos en pulgadas
})

# Cargar el dataset
df = pd.read_csv('Semana7/notas_1u.csv')

# Estadísticas generales
print("📊 Estadísticas Generales:")
print(df['Nota'].describe().to_string())
print("\n🧪 Promedio de Nota por Tipo de Examen:")
promedio_por_tipo = df.groupby('Tipo_Examen')['Nota'].mean()
print(promedio_por_tipo.to_string())
# Nota mínima por tipo de examen
nota_minima_por_tipo = df.groupby('Tipo_Examen')['Nota'].min()
print("\n🔻 Nota Mínima por Tipo de Examen:")
print(nota_minima_por_tipo.to_string())


# Histograma de la distribución de notas
plt.figure()
sns.histplot(df['Nota'], kde=True, bins=10, color='#1f77b4')
plt.title('🎓 Distribución de Notas')
plt.xlabel('Nota')
plt.ylabel('Frecuencia')
plt.tight_layout()
plt.show()

# Boxplot por tipo de examen
plt.figure()
sns.boxplot(data=df, x='Tipo_Examen', y='Nota', palette='viridis')
plt.title('📦 Boxplot de Notas por Tipo de Examen')
plt.xlabel('Tipo de Examen')
plt.ylabel('Nota')
plt.tight_layout()
plt.show()

# Gráfico de barras: promedio por tipo de examen
plt.figure()
sns.barplot(x=promedio_por_tipo.index, y=promedio_por_tipo.values, palette='rocket')
plt.title('📈 Promedio de Notas por Tipo de Examen')
plt.xlabel('Tipo de Examen')
plt.ylabel('Nota Promedio')
plt.ylim(0, 20)
for i, v in enumerate(promedio_por_tipo.values):
    plt.text(i, v + 0.5, f"{v:.2f}", ha='center', fontweight='bold')
plt.tight_layout()
plt.show()
