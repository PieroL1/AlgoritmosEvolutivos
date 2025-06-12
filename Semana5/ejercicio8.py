import pandas as pd
import numpy as np
import random
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
from deap import base, creator, tools
import matplotlib.pyplot as plt

# ------------------ Cargar y preparar datos ------------------

file_path = r'Semana5\ejercicio8.xlsx'  # RAW string para evitar errores de barra
df = pd.read_excel(file_path)

X = df[['Rooms', 'Area_m2']].values
y = df['Price_Soles'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ------------------ Configuración DEAP ------------------

# Borrar registros previos si re-ejecutas el código
if "FitnessMin" in creator.__dict__:
    del creator.FitnessMin
if "Individual" in creator.__dict__:
    del creator.Individual

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Rango para alpha y max_iter
ALPHA_MIN, ALPHA_MAX = 0.001, 10
R_MIN, R_MAX = 10, 1000

toolbox.register("attr_alpha", random.uniform, ALPHA_MIN, ALPHA_MAX)
toolbox.register("attr_r", random.uniform, R_MIN, R_MAX)

toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_alpha, toolbox.attr_r), n=1)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def eval_ridge(ind):
    alpha = ind[0]
    max_iter = max(int(ind[1]), 10)
    model = Ridge(alpha=alpha, max_iter=max_iter, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, preds)  # RMSE correcto
    return (rmse,)

toolbox.register("evaluate", eval_ridge)

def mutate(ind, mu=0, sigma=0.1, indpb=0.5):
    if random.random() < indpb:
        ind[0] += random.gauss(mu, sigma)
        ind[0] = max(ALPHA_MIN, min(ind[0], ALPHA_MAX))
    if random.random() < indpb:
        ind[1] += random.gauss(0, 10)
        ind[1] = max(R_MIN, min(ind[1], R_MAX))
    return (ind,)

toolbox.register("mutate", mutate)
toolbox.register("select", tools.selBest)

# ------------------ Algoritmo Evolutivo Hill Climber ------------------

def main():
    pop_size = 20
    ngen = 50
    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("min", np.min)
    stats.register("avg", np.mean)

    log = tools.Logbook()
    log.header = ["gen", "min", "avg"]

    # Evaluar población inicial
    for ind in pop:
        ind.fitness.values = toolbox.evaluate(ind)

    for gen in range(ngen):
        # Selección greedy (mejores)
        offspring = toolbox.select(pop, k=10)

        # Reproducción por clonación + mutación
        new_pop = []
        while len(new_pop) < pop_size:
            ind = toolbox.clone(random.choice(offspring))
            toolbox.mutate(ind)
            ind.fitness.values = toolbox.evaluate(ind)
            new_pop.append(ind)

        pop = new_pop
        hof.update(pop)
        record = stats.compile(pop)
        log.record(gen=gen, **record)
        print(log.stream)

    # ------------------ Resultados ------------------
    best = hof[0]
    print("\n--- Mejor Solución ---")
    print(f"Alpha óptimo: {best[0]:.4f}")
    print(f"max_iter óptimo: {int(best[1])}")
    print(f"RMSE: {best.fitness.values[0]:.4f}")

    # Curva de convergencia
    plt.plot(log.select("gen"), log.select("min"), label="Min RMSE")
    plt.plot(log.select("gen"), log.select("avg"), label="Avg RMSE")
    plt.xlabel("Generación")
    plt.ylabel("RMSE")
    plt.title("Curva de convergencia")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
