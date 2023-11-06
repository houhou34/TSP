import random
import math

# 城市坐标
coordinates = [(41, 94), (37, 84), (54, 67), (25, 62), (7, 64), (2, 99),
               (68, 58), (71, 44), (54, 62), (83, 69), (64, 60), (18, 54),
               (22, 60), (83, 46), (91, 38), (25, 38), (24, 42), (58, 69),
               (71, 71), (74, 78), (87, 76), (18, 40), (13, 40), (82, 7),
               (62, 32), (58, 35), (45, 21), (41, 26), (44, 35), (4, 50)]

# 计算两点间的欧几里得距离
def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# 评估路径的适应度
def fitness(path):
    total_distance = 0
    for i in range(len(path)):
        total_distance += euclidean_distance(coordinates[path[i]], coordinates[path[(i + 1) % len(path)]])
    return 1 / total_distance

# 选择（锦标赛选择）
def select(population, fitnesses, tournament_size=5):
    tournament = random.sample(list(zip(population, fitnesses)), tournament_size)
    tournament.sort(key=lambda x: x[1], reverse=True)
    return tournament[0][0]

# 交叉（部分映射交叉 PMX）
def pmx(parent1, parent2):
    size = len(parent1)
    p1, p2 = [0]*size, [0]*size

    # Initialize the position of each indices in the individuals
    for i in range(size):
        p1[parent1[i]] = i
        p2[parent2[i]] = i

    # Choose crossover points
    cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))

    # Apply crossover between cx points
    for i in range(cxpoint1, cxpoint2):
        temp1 = parent1[i]
        temp2 = parent2[i]

        parent1[i], parent2[i] = temp2, temp1
        p1[temp1], p1[temp2] = p1[temp2], p1[temp1]
        p2[temp1], p2[temp2] = p2[temp2], p2[temp1]

    # Map the remaining elements of the parent
    for i in range(size):
        if i < cxpoint1 or i >= cxpoint2:
            while parent1[i] != parent2[p1[parent1[i]]]:
                parent1[i] = parent2[p1[parent1[i]]]

            while parent2[i] != parent1[p2[parent2[i]]]:
                parent2[i] = parent1[p2[parent2[i]]]

    return parent1, parent2

# 变异（逆转变异）
def mutate(chromosome, mutation_rate):
    if random.random() < mutation_rate:
        start, end = sorted(random.sample(range(len(chromosome)), 2))
        while start < end:
            chromosome[start], chromosome[end] = chromosome[end], chromosome[start]
            start += 1
            end -= 1

# 遗传算法
def genetic_algorithm(coordinates, population_size=100, generations=500, mutation_rate=0.02):
    # 初始种群
    population = [random.sample(range(len(coordinates)), len(coordinates)) for _ in range(population_size)]
    best_path = None
    best_fitness = 0

    for _ in range(generations):
        fitnesses = [fitness(chromosome) for chromosome in population]

        new_population = []
        for i in range(0, population_size, 2):
            parent1 = select(population, fitnesses)
            parent2 = select(population, fitnesses)

            child1, child2 = pmx(parent1.copy(), parent2.copy())

            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)

            new_population.extend([child1, child2])

        population = new_population

        # 记录最佳路径
        current_best = max(population, key=fitness)
        current_best_fitness = fitness(current_best)
        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_path = current_best

    return best_path, 1 / best_fitness

# 主程序
best_path, min_distance = genetic_algorithm(coordinates)
print("最短路径长度:", min_distance)
print("访问顺序:", best_path)
