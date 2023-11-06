import math
from queue import PriorityQueue
from tqdm import tqdm

# 城市坐标
coordinates = [(41, 94), (37, 84), (54, 67), (25, 62), (7, 64), (2, 99),
               (68, 58), (71, 44), (54, 62), (83, 69), (64, 60), (18, 54),
               (22, 60), (83, 46), (91, 38), (25, 38), (24, 42), (58, 69),
               (71, 71), (74, 78), (87, 76), (18, 40), (13, 40), (82, 7),
               (62, 32), (58, 35), (45, 21), (41, 26), (44, 35), (4, 50)]

# 计算两点间的欧几里得距离
def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

# 构建距离矩阵
def distance_matrix(coords):
    n = len(coords)
    dist_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = euclidean_distance(coords[i], coords[j])
    return dist_matrix

# 分支定界算法寻找TSP最短路径
def branch_and_bound(dist_matrix):
    n = len(dist_matrix)
    pq = PriorityQueue()
    pq.put((0, [0], 0))  # 初始节点：成本，路径，最后访问的城市
    min_cost = float('inf')
    best_path = []

    # 进度条初始化
    pbar = tqdm(total=n*(n-1)/2, desc='处理节点')

    while not pq.empty():
        cost, path, last = pq.get()
        pbar.update(1)  # 更新进度条

        if cost > min_cost:
            continue

        if len(path) == n:
            if cost < min_cost:
                min_cost = cost
                best_path = path
            continue

        for i in range(n):
            if i not in path:
                new_cost = cost + dist_matrix[last][i]
                pq.put((new_cost, path + [i], i))

    pbar.close()
    return min_cost, best_path

# 主程序
dist_matrix = distance_matrix(coordinates)
min_cost, best_path = branch_and_bound(dist_matrix)
print("最短路径长度:", min_cost)
print("访问顺序:", best_path)
