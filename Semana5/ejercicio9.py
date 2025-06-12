import pandas as pd
import numpy as np
from deap import base, creator, tools, algorithms
from sklearn.metrics import f1_score
import random
import matplotlib.pyplot as plt

# --- Cargar datos ---
file_path = r'Semana5\ejercicio9.xlsx'
df = pd.read_excel(file_path)
X = df.iloc[:, :-1].values  # las 5 características
y = df.iloc[:, -1].values   # clase (0: ham, 1: spam)

# --- Dividir en entrenamiento y validación ---
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)

# --- Definiciones DEAP ---
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Genotipo: 5 pesos + 1 umbral
toolbox.register("attr_float", lambda: random.uniform(-5.0, 5.0))  # pesos
toolbox.register("attr_threshold", lambda: random.uniform(0.0, 1.0))  # umbral
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_float, toolbox.attr_float, toolbox.attr_float, toolbox.attr_float, toolbox.attr_float, toolbox.attr_threshold),
                 n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    weights = np.array(individual[:5])
    threshold = individual[5]
    scores = X_train.dot(weights)
    preds = (scores > threshold).astype(int)
    if preds.sum() == 0 or preds.sum() == len(preds):
        return 0.0,  # F1 indefinido
    return f1_score(y_train, preds),  # Fitness: F1-score

# Hill Climbing local
def hill_climb(ind, steps=10, alpha=0.05):
    best = ind[:]
    best_fit = evaluate(best)[0]
    for _ in range(steps):
        trial = [gene + random.uniform(-alpha, alpha) for gene in best]
        trial[5] = min(max(trial[5], 0.0), 1.0)  # umbral en [0,1]
        fit = evaluate(trial)[0]
        if fit > best_fit:
            best = trial
            best_fit = fit
    ind[:] = best
    return ind

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxBlend, alpha=0.4)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.5)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    pop = toolbox.population(n=30)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", np.mean)
    stats.register("max", np.max)
    
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    f1_progress = []
    
    NGEN = 40
    for gen in range(NGEN):
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        # Reproducción
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < 0.9:
                toolbox.mate(child1, child2)
                del child1.fitness.values, child2.fitness.values

        for mutant in offspring:
            if random.random() < 0.3:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Hill Climbing por individuo
        for i in range(len(offspring)):
            if not offspring[i].fitness.valid:
                offspring[i] = hill_climb(offspring[i])

        # Evaluar fitness
        invalid = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid))
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring
        hof.update(pop)

        # Registro estadístico
        record = stats.compile(pop)
        f1_progress.append(record["max"])
        print(f"Gen {gen:02d} | F1 max: {record['max']:.4f} | F1 avg: {record['avg']:.4f}")

    print("\n--- Mejor solución encontrada ---")
    best = hof[0]
    print(f"Pesos: {best[:5]}")
    print(f"Umbral: {best[5]:.4f}")

    # Evaluar en conjunto de validación
    weights = np.array(best[:5])
    threshold = best[5]
    scores = X_val.dot(weights)
    preds = (scores > threshold).astype(int)
    f1_val = f1_score(y_val, preds)
    print(f"F1 en validación: {f1_val:.4f}")

    # Gráfica F1 vs generación
    plt.plot(f1_progress)
    plt.title("F1-score vs generación")
    plt.xlabel("Generación")
    plt.ylabel("F1-score")
    plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
