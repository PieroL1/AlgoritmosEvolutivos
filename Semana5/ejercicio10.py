import pandas as pd
import numpy as np
import random
from deap import base, creator, tools
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# --- Cargar datos ---
df = pd.read_excel("Semana5\ejercicio10.xlsx")

# Asumimos que la última columna es la clase (Alta, Media, Baja)
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values

# Codificar etiquetas (Alta=0, Media=1, Baja=2 por ejemplo)
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Escalar características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir train/val
X_train, X_val, y_train, y_val = train_test_split(X_scaled, y_encoded, test_size=0.3, random_state=42)

# Convertir a tensores
X_train_t = torch.tensor(X_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.long)
X_val_t = torch.tensor(X_val, dtype=torch.float32)
y_val_t = torch.tensor(y_val, dtype=torch.long)

# --- Definir red neuronal dinámica ---
class MiniNet(nn.Module):
    def __init__(self, input_dim, n_layers, neurons_per_layer):
        super(MiniNet, self).__init__()
        layers = []
        last_dim = input_dim
        for i in range(n_layers):
            layers.append(nn.Linear(last_dim, neurons_per_layer[i]))
            layers.append(nn.ReLU())
            last_dim = neurons_per_layer[i]
        layers.append(nn.Linear(last_dim, 3))  # 3 clases
        self.net = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.net(x)

# --- Genotipo ---
# [n_layers (1-3 int), neurons_layer1 (5-50 int), neurons_layer2 (5-50 int), neurons_layer3 (5-50 int), learning_rate (float 0.0001-0.1)]

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("n_layers", lambda: random.randint(1,3))
toolbox.register("neurons", lambda: random.randint(5,50))
toolbox.register("learning_rate", lambda: random.uniform(0.0001, 0.1))

def create_individual():
    n_layers = toolbox.n_layers()
    neurons = [toolbox.neurons() for _ in range(3)]  # 3 capas posibles
    lr = toolbox.learning_rate()
    return creator.Individual([n_layers] + neurons + [lr])

toolbox.register("individual", create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# --- Evaluación ---
def evaluate(individual):
    n_layers = individual[0]
    neurons = individual[1:4][:n_layers]
    lr = individual[4]

    model = MiniNet(X_train.shape[1], n_layers, neurons)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # Entrenamiento breve: 20 epochs
    model.train()
    for epoch in range(20):
        optimizer.zero_grad()
        outputs = model(X_train_t)
        loss = criterion(outputs, y_train_t)
        loss.backward()
        optimizer.step()

    # Evaluar accuracy en validación
    model.eval()
    with torch.no_grad():
        outputs = model(X_val_t)
        preds = torch.argmax(outputs, dim=1).numpy()
    acc = accuracy_score(y_val, preds)
    return acc,

# --- Mutación (ajustes pequeños) ---
def mutate(individual):
    # Mutar n_layers
    if random.random() < 0.3:
        individual[0] = max(1, min(3, individual[0] + random.choice([-1,1])))
    # Mutar neuronas
    for i in range(1,4):
        if random.random() < 0.5:
            individual[i] = max(5, min(50, individual[i] + random.choice([-3,-2,-1,1,2,3])))
    # Mutar learning rate
    if random.random() < 0.5:
        individual[4] = min(0.1, max(0.0001, individual[4] + random.uniform(-0.005,0.005)))
    return individual,

# --- Hill climbing local ---
def hill_climb(ind, steps=5):
    best = ind[:]
    best_fit = evaluate(best)[0]
    for _ in range(steps):
        trial = best[:]
        # Pequeños ajustes como mutar
        trial, = mutate(trial)
        fit = evaluate(trial)[0]
        if fit > best_fit:
            best = trial
            best_fit = fit
    ind[:] = best
    return ind

toolbox.register("evaluate", evaluate)
toolbox.register("mutate", mutate)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(42)
    pop = toolbox.population(n=20)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", np.mean)
    stats.register("max", np.max)

    # Evaluar población inicial
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    acc_progress = []

    NGEN = 25
    for gen in range(NGEN):
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        # Mutación + Hill climbing
        for mutant in offspring:
            if random.random() < 0.8:
                toolbox.mutate(mutant)
                del mutant.fitness.values
            # Hill climbing local
            mutant = hill_climb(mutant)
        
        # Evaluar fitness
        invalid = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid))
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring
        hof.update(pop)

        record = stats.compile(pop)
        acc_progress.append(record["max"])
        print(f"Gen {gen:02d} | Accuracy max: {record['max']:.4f} | Accuracy avg: {record['avg']:.4f}")

    # Resultados
    best = hof[0]
    n_layers = best[0]
    neurons = best[1:4][:n_layers]
    lr = best[4]

    print("\n--- Mejor arquitectura encontrada ---")
    print(f"Número de capas: {n_layers}")
    print(f"Neuronas por capa: {neurons}")
    print(f"Tasa de aprendizaje: {lr:.5f}")

    # Evaluar accuracy final en validación
    model = MiniNet(X_train.shape[1], n_layers, neurons)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    model.train()
    for epoch in range(20):
        optimizer.zero_grad()
        outputs = model(X_train_t)
        loss = criterion(outputs, y_train_t)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        outputs = model(X_val_t)
        preds = torch.argmax(outputs, dim=1).numpy()
    acc_val = accuracy_score(y_val, preds)
    print(f"Accuracy en validación: {acc_val:.4f}")

    # Gráfica Accuracy vs generación
    plt.plot(acc_progress)
    plt.title("Accuracy vs generación")
    plt.xlabel("Generación")
    plt.ylabel("Accuracy")
    plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
