import ga
import gbexp
import random

if __name__ == "__main__":
    '''
    N = 4
    V = 6
    alpha = 0
    l = {}     # 箱子宽
    c = {}     # 箱子高
    p = {}
    l[1], c[1] = 6, 11
    l[2], c[2] = 6, 12
    l[3], c[3] = 4, 12
    l[4], c[4] = 5, 14
    l[5], c[5] = 5, 16
    l[6], c[6] = 3, 4
    l[7], c[7] = 3, 5
    l[8], c[8] = 2, 6 
    l[9], c[9] = 4, 7
    l[10], c[10] = 4, 8
    l[11], c[11] = 5, 6
    # l[8], c[8] = 2, 6
    # l[9], c[9] = 4, 7
    # l[10], c[10] = 5, 8
    # l[11], c[11] = 5, 6
    tide = [1, 3, 5, 7, 9, 11]
    a = {}
    a[1] = 1
    a[2] = 5
    a[3] = 8
    a[4] = 12
    a[5] = 14
    a[6] = 16
    a[7] = 17
    a[8] = 19
    a[9] = 21
    a[10] = 25
    a[11] = 28
    q_max = {}
    q_min = {}
    p = {}
    for i in range(1, 12):
        q_max[i] = 6
        q_min[i] = 1
        p[i] = 3
    B = 11
    L = 10
    Q = 7
    # 先生成初始解
    pop = ga.init_pop(100, B, L, c, q_max, q_min, l)
    best_ans = []
    default = 0
    best_pop = []
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
            best_pop = pop[best_index]
        if i % 100 == 0:
            print('best obj is ' + str(best_obj))
            print(best_ans)
            print(best_pop)
            print('-----------------------------------------------------------------')
        pop_select = ga.select(pop, decoding_fitness, 50)
        pop_crossover = ga.crossover(pop_select, 50)
        pop_mutation = ga.mutation(pop_crossover, l, q_min, q_max, 0.5, L, c)
        pop = pop_select + pop_mutation
    print(best_ans)
    print(best_pop)
    '''
    gurobi_time = []
    gurobi_res = []
    gurobi_pcg = []
    ga_time = []
    ga_res = []
    al_exp = [0,0.1,0.2,0.3,0.4,0.5,1,2]
    for B in [10,13,15,20]:
        print('------------------------------B=' + str(B))
        for k in range(10): #试验次数
            print('-----------------------' + str(B) + '第几次' + str(k))
            l = {}     # 箱子宽
            c = {}     # 箱子高
            p = {}
            N = 7
            Q = 7
            L = 20
            n_small = B // 3
            n_mid = B //3
            n_large = B - n_small - n_mid
            tmp_w = []
            tmp_c = []
            for i in range(1, n_small + 1):
                l[i] = random.randint(1, 3)
                c[i] = random.randint(3, 6)
                p[i] = random.randint(0, L - l[i] + 1)
            for i in range(n_small + 1, n_small + n_mid + 1):
                l[i] = random.randint(4, 6)
                c[i] = random.randint(7, 11)
                p[i] = random.randint(0, L - l[i] + 1)
            for i in range(n_small + n_mid + 1, B + 1):
                l[i] = random.randint(7, 9)
                c[i] = random.randint(12, 16)
                p[i] = random.randint(0, L - l[i] + 1)
            a_max = int(8*N)
            a = {}
            for i in range(1, B + 1):
                a[i] = random.randint(1, a_max)
            tide = [1, 3, 5, 7,9]
            free = [2, 4, 6, 8, 10]
            q_max = {}
            q_min = {}
            for i in range(1, B + 1):
                q_max[i] = random.randint(int(Q/2),Q - 1)
                q_min[i] = 1
            variables = {}
            variables['B'] = B
            variables['L'] = L
            variables['Q'] = Q
            variables['N'] = N
            variables['V'] = 6
            variables['q_max'] = q_max
            variables['q_min'] = q_min
            variables['a'] = a
            variables['l'] = l
            variables['c'] = c
            variables['tide'] = tide
            variables['free'] = free
            # variables['alpha'] = 0
            variables['p'] = p
            for alp in al_exp:
                variables['alpha'] = alp
                result = gbexp.gb_solver(variables)
                for _ in range(10):
                    a, b = ga.ga_algorithm(variables)
                    ga_res.append(a)
                    ga_time.append(b)
                    print(b)
                gurobi_time.append(result['Runtime'])
                gurobi_res.append(result['Obj'])
                gurobi_pcg.append(result['pcount'])
                print(ga_res)
                print(ga_time)
                print(gurobi_pcg)
                print(gurobi_res)
                print(gurobi_time)
    print(gurobi_pcg)
    print(gurobi_res)
    print(gurobi_time)
    '''
        l[1], c[1] = 6, 8
        l[2], c[2] = 7, 12
        l[3], c[3] = 4, 10
        l[4], c[4] = 4, 16
        l[5], c[5] = 5, 15
        l[6], c[6] = 6, 5
        l[7], c[7] = 3, 4
        l[8], c[8] = 2, 6 
        l[9], c[9] = 4, 7
        l[10], c[10] = 5, 8
        l[11], c[11] = 4, 6
        
        # l[8], c[8] = 2, 6
        # l[9], c[9] = 4, 7
        # l[10], c[10] = 5, 8
        # l[11], c[11] = 5, 6
        tide = [1, 3, 5, 7, 9, 11]
        free = [2, 4, 6, 8, 10]
        a = {}
        a[1] = 1
        a[2] = 4
        a[3] = 7
        a[4] = 13
        a[5] = 15
        a[6] = 16
        a[7] = 16
        a[8] = 18
        a[9] = 20
        a[10] = 24
        a[11] = 28
        q_max = {}
        q_min = {}
        p = {}
        
        p[1] = 2
        p[2] = 3
        p[3] = 5
        p[4] = 6
        p[5] = 3
        p[6] = 4
        p[7] = 4
        p[8] = 7
        p[9] = 6    
        p[10] = 5
        p[11] = 1
        
        for i in range(1, 12):
            q_max[i] = 6
            q_min[i] = 1
            # p[i] = 3
        B = 11
        L = 10
        Q = 7
        '''
    '''
        l = {}     # 箱子宽
        c = {}     # 箱子高
        p = {}     # 箱子偏好位置
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
        free = [5, 6, 7]
        a = {}
        a[1] = 1
        a[2] = 5
        a[3] = 8
        a[4] = 12
        a[5] = 2
        a[6] = 3
        a[7] = 7
        # a[8] = 19
        # a[9] = 21
        # a[10] = 25
        # a[11] = 28
        q_max = {}
        q_min = {}
        p = {}
        for i in range(1, 8):
            q_max[i] = 4
            q_min[i] = 1
            p[i] = 1
        '''
    '''
        variables = {}
        variables['B'] = 11
        variables['L'] = 10
        variables['Q'] = 7
        variables['N'] = 4
        variables['V'] = 6
        variables['q_max'] = q_max
        variables['q_min'] = q_min
        variables['a'] = a
        variables['l'] = l
        variables['c'] = c
        variables['tide'] = tide
        variables['free'] = free
        # variables['alpha'] = 0
        variables['p'] = p
        beixuan = [0,0.1,0.2,0,3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5]
        objguro = []
        objga = []
        pcguro = []
        pcga = []
        variables['alpha'] = 1
        tmp_result = gbexp.gb_solver(variables)
        
        print(tmp_result)
        print(p)
        '''
    '''
        for alpha in beixuan:
            variables['alpha'] = alpha
            print('-----------------------------------alpha = ' + str(alpha) + '-----------------------------------------------')
            a, b = ga.ga_algorithm(variables)
            objga.append(a)
            pcga.append(b)
            tmp_result = gbexp.gb_solver(variables)
            objguro.append(tmp_result['Obj'])
            pcguro.append(tmp_result['pcount'])
        print(objga)
        print(objguro)
        print(pcguro)
        print(pcga)
    '''