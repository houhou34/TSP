import random
import math

# 城市坐标
coordinates = [(41, 94), (37, 84), (54, 67), (25, 62), (7, 64), (2, 99),
               (68, 58), (71, 44), (54, 62), (83, 69), (64, 60), (18, 54),
               (22, 60), (83, 46), (91, 38), (25, 38), (24, 42), (58, 69),
               (71, 71), (74, 78), (87, 76), (18, 40), (13, 40), (82, 7),
               (62, 32), (58, 35), (45, 21), (41, 26), (44, 35), (4, 50)]

# PSO参数
num_particles = 50
num_iterations = 200
w = 0.5  # 惯性权重
c1 = 1.5 # 个体学习因子
c2 = 2.0 # 社会学习因子

# 计算两点间的欧几里得距离
def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# 计算路径长度
def path_length(path, coords):
    total_length = 0
    for i in range(len(path)):
        total_length += euclidean_distance(coords[path[i]], coords[path[(i + 1) % len(path)]])
    return total_length

# 2-opt局部搜索优化
def two_opt_swap(route):
    best_route = route
    best_distance = path_length(route, coordinates)
    for i in range(len(route) - 1):
        for j in range(i + 2, len(route)):
            if j - i == 1: continue  # 相邻城市不交换
            new_route = route[:i] + route[i:j][::-1] + route[j:]
            new_distance = path_length(new_route, coordinates)
            if new_distance < best_distance:
                best_distance = new_distance
                best_route = new_route
    return best_route

# 初始化粒子
def initialize_particles(num_particles, num_cities):
    particles = []
    for _ in range(num_particles):
        particle = list(range(num_cities))
        random.shuffle(particle)
        particles.append(particle)
    return particles

# 更新粒子
def update_particle(particle, pBest, gBest):
    new_particle = particle.copy()
    for _ in range(int(w * len(particle))):  # 按照惯性权重随机交换
        swap = sorted(random.sample(range(len(particle)), 2))
        new_particle[swap[0]], new_particle[swap[1]] = new_particle[swap[1]], new_particle[swap[0]]

    if random.random() < c1:  # 向个体最优靠拢
        swap = sorted(random.sample(range(len(particle)), 2))
        if pBest[swap[0]] in new_particle and pBest[swap[1]] in new_particle:
            idx1, idx2 = new_particle.index(pBest[swap[0]]), new_particle.index(pBest[swap[1]])
            new_particle[idx1], new_particle[idx2] = new_particle[idx2], new_particle[idx1]

    if random.random() < c2:  # 向全局最优靠拢
        swap = sorted(random.sample(range(len(particle)), 2))
        if gBest[swap[0]] in new_particle and gBest[swap[1]] in new_particle:
            idx1, idx2 = new_particle.index(gBest[swap[0]]), new_particle.index(gBest[swap[1]])
            new_particle[idx1], new_particle[idx2] = new_particle[idx2], new_particle[idx1]

    return new_particle

# 粒子群优化算法
def particle_swarm_optimization(coords, num_particles, num_iterations):
    num_cities = len(coords)
    particles = initialize_particles(num_particles, num_cities)
    pBest = particles.copy()
    gBest = min(particles, key=lambda x: path_length(x, coords))

    for _ in range(num_iterations):
        for i, particle in enumerate(particles):
            # 更新粒子位置
            particles[i] = update_particle(particle, pBest[i], gBest)

            # 更新个体最优
            if path_length(particles[i], coords) < path_length(pBest[i], coords):
                pBest[i] = particles[i]

        # 更新全局最优
        current_gBest = min(particles, key=lambda x: path_length(x, coords))
        if path_length(current_gBest, coords) < path_length(gBest, coords):
            gBest = current_gBest

        # 对全局最优进行2-opt局部搜索
        gBest = two_opt_swap(gBest)

    return gBest, path_length(gBest, coords)

# 执行PSO
best_path, min_length = particle_swarm_optimization(coordinates, num_particles, num_iterations)
print("最短路径长度:", min_length)
print("访问顺序:", best_path)


