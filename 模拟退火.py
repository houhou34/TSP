import math
import random


# 定义计算两点间欧几里得距离的函数
def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


# 定义计算路径总距离的函数
def total_distance(path, cities):
    return sum(distance(cities[path[i]], cities[path[(i + 1) % len(path)]]) for i in range(len(path)))


# 产生初始解：随机打乱城市顺序
def initial_solution(cities):
    path = list(range(len(cities)))
    random.shuffle(path)
    return path


# 产生邻域解：交换路径中的两个城市
def get_neighbour(path):
    a, b = random.sample(range(len(path)), 2)
    path[a], path[b] = path[b], path[a]
    return path


# 模拟退火算法
def simulated_annealing(cities, temperature=10000, cooling_rate=0.995, stop_temperature=0.0000001):
    current_solution = initial_solution(cities)
    current_distance = total_distance(current_solution, cities)
    best_solution = current_solution
    best_distance = current_distance

    while temperature > stop_temperature:
        new_solution = get_neighbour(current_solution[:])
        new_distance = total_distance(new_solution, cities)

        # 接受新解的条件：更短或者满足概率条件
        if (new_distance < current_distance or
                random.random() < math.exp((current_distance - new_distance) / temperature)):
            current_solution = new_solution
            current_distance = new_distance

            # 检查是否是最优解
            if current_distance < best_distance:
                best_solution = current_solution
                best_distance = current_distance

        # 降低温度
        temperature *= cooling_rate
        print(temperature)
        print(cooling_rate)

    return best_solution, best_distance


# 定义30个城市的坐标
cities_coordinates = [
    (41, 94), (37, 84), (54, 67), (25, 62), (7, 64), (2, 99),
    (68, 58), (71, 44), (54, 62), (83, 69), (64, 60), (18, 54),
    (22, 60), (83, 46), (91, 38), (25, 38), (24, 42), (58, 69),
    (71, 71), (74, 78), (87, 76), (18, 40), (13, 40), (82, 7),
    (62, 32), (58, 35), (45, 21), (41, 26), (44, 35), (4, 50)
]

# 运行模拟退火算法
best_solution, best_distance = simulated_annealing(cities_coordinates)

# 打印最优解及其距离
print("Best solution:", best_solution)
print("Best distance:", best_distance)
