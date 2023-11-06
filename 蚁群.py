import random
import math
from operator import attrgetter

# 城市坐标
coordinates = [(41, 94), (37, 84), (54, 67), (25, 62), (7, 64), (2, 99),
               (68, 58), (71, 44), (54, 62), (83, 69), (64, 60), (18, 54),
               (22, 60), (83, 46), (91, 38), (25, 38), (24, 42), (58, 69),
               (71, 71), (74, 78), (87, 76), (18, 40), (13, 40), (82, 7),
               (62, 32), (58, 35), (45, 21), (41, 26), (44, 35), (4, 50)]

# 计算两点间的欧几里得距离
def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# 路径类
class Path:
    def __init__(self):
        self.route = random.sample(range(len(coordinates)), len(coordinates))
        self.distance = self.calculate_distance()

    # 计算路径长度
    def calculate_distance(self):
        total_distance = 0
        for i in range(len(self.route)):
            from_city = self.route[i]
            to_city = self.route[(i + 1) % len(self.route)]
            total_distance += euclidean_distance(coordinates[from_city], coordinates[to_city])
        return total_distance

# 遗传算法类
class GeneticAlgorithm:
    def __init__(self, population_size=100, mutation_rate=0.01, generations=500):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = [Path() for _ in range(population_size)]

    # 进化过程
    def evolve(self):
        for _ in range(self.generations):
            self.selection()
            self.crossover()
            self.mutation()

    # 选择过程
    def selection(self):
        self.population.sort(key=attrgetter('distance'))
        self.population = self.population[:self.population_size//2]

    # 交叉过程
    def crossover(self):
        offspring = []
        for _ in range(self.population_size - len(self.population)):
            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population)
            child = self.crossover_paths(parent1, parent2)
            offspring.append(child)
        self.population.extend(offspring)

    # 交叉两条路径
    def crossover_paths(self, parent1, parent2):
        child = Path()
        child.route = []

        gene_a = int(random.random() * len(parent1.route))
        gene_b = int(random.random() * len(parent1.route))

        start_gene = min(gene_a, gene_b)
        end_gene = max(gene_a, gene_b)

        for i in range(start_gene, end_gene):
            child.route.append(parent1.route[i])

        child.route += [item for item in parent2.route if item not in child.route]

        child.distance = child.calculate_distance()
        return child

    # 变异过程
    def mutation(self):
        for path in self.population:
            if random.random() < self.mutation_rate:
                self.mutate_path(path)

    # 变异一条路径
    def mutate_path(self, path):
        index1 = int(random.random() * len(path.route))
        index2 = int(random.random() * len(path.route))

        path.route[index1], path.route[index2] = path.route[index2], path.route[index1]
        path.distance = path.calculate_distance()

# 运行遗传算法
ga = GeneticAlgorithm()
ga.evolve()

# 获取最佳路径
best_path = min(ga.population, key=attrgetter('distance'))
print("最短路径长度:", best_path.distance)
print("访问顺序:", best_path.route)
