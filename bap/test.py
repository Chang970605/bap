import ga

if __name__ == "__main__":
    N = 4
    V = 6
    alpha = 3
    l = {}     # 箱子宽
    c = {}     # 箱子高
    p = {}
    l[1], c[1] = 3, 4
    l[2], c[2] = 3, 6
    l[3], c[3] = 2, 6
    l[4], c[4] = 4, 7
    l[5], c[5] = 4, 8
    l[6], c[6] = 5, 7
    l[7], c[7] = 3, 5
    # l[8], c[8] = 2, 6
    # l[9], c[9] = 4, 7
    # l[10], c[10] = 5, 8
    # l[11], c[11] = 5, 6
    tide = [1, 2, 3, 4]
    a = {}
    a[1] = 1
    a[2] = 5
    a[3] = 8
    a[4] = 12
    a[5] = 2
    a[6] = 3
    a[7] = 7
    q_max = {}
    q_min = {}
    p = {}
    for i in range(1, 8):
        q_max[i] = 4
        q_min[i] = 1
        p[i] = 3
    B = 7
    L = 8
    Q = 7
    # 先生成初始解
    pop = ga.init_pop(100, B, L, c, q_max, q_min, l)
    best_ans = []
    default = 0
    for i in range(1, B + 1):
        default += (2 * N * V - a[i])
        default += (alpha * max(abs(p[i] - 1), abs(L - p[i])))
    best_obj = default
    for i in range(500):
        decoding_pop = ga.translate(pop, N, V, alpha, l, L, tide, B, a, p, c, Q, q_min, q_max)
        decoding_fitness = ga.get_fitness(decoding_pop, alpha, default)
        best_index = decoding_fitness.index(max(decoding_fitness))
        if 1 / decoding_fitness[best_index] < best_obj:
            best_obj = (1 / decoding_fitness[best_index])
            best_ans = decoding_pop[best_index]
        if i % 100 == 0:
            print('best obj is ' + str(best_obj))
        pop_select = ga.select(pop, decoding_fitness, 50)
        pop_crossover = ga.crossover(pop_select, 50)
        pop_mutation = ga.mutation(pop_crossover, l, q_min, q_max, 0.5, L, c)
        pop = pop_select + pop_mutation
    print(best_ans)