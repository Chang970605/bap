import ha
import random
import gbexp
import time
# x,y,w,h
# p = [[0, 0, 0, 0],[0.3,0,0.3,4],[0.7,0,0.3,5],[0,0,0.3,6],[0.3,4,0.3,4],[0.75,5,0.25,4],[0,6,0.25,4]]
# w = 0.3
# h = 3
# W = 1
# print(ha.find_position(p,w,h,W))
beixuan = [0.1 * i for i in range(1,31)]
compare_resultone = {}
compare_resultotwo = {}
compare_resultothree = {}
for i in beixuan:
    compare_resultone[i] = 0
    compare_resultotwo[i] = 0
    compare_resultothree[i] = 0

for kk in range(10):
    w = {}     # 箱子宽
    h = {}     # 箱子高
    p = {}     # 箱子偏好位置
    '''
    w[1], h[1] = 2, 5
    w[2], h[2] = 3, 5
    w[3], h[3] = 3, 6
    w[4], h[4] = 3, 6
    w[5], h[5] = 3, 7
    w[6], h[6] = 5, 7
    w[7], h[7] = 5, 12
    w[8], h[8] = 7, 12
    w[9], h[9] = 8, 12
    w[10], h[10] = 9, 14
    '''
    n = 12
    ww = []
    hh = []
    for _ in range(n):
        ww.append(random.randint(0, 15))
        hh.append(random.randint(0, 20))
    ww.sort()
    hh.sort()
    ww = ww[::-1]
    hh = hh[::-1]
    # ww = list(w.values())[::-1]
    # hh = list(h.values())[::-1]
    for j in range(1, 13):
        p[j] = random.randint(0, 20 - ww[j - 1])
        w[j] = ww[j - 1]
        h[j] = hh[j - 1]
    variables = {}
    variables['N'] = n
    variables['W'] = 20
    variables['w'] = w
    variables['h'] = h
    variables['alpha'] = 1
    variables['p'] = p
    pp = list(p.values())
    #he_strat = time.time()
    he_result = ha.ffd(ww, hh, 20, pp)
    he_resulttwo = ha.ffdtwo(ww, hh, 20, pp)
    he_resultthree = ha.ffdthree(ww, hh, 20, pp)
    for al in beixuan:
        variables['alpha'] = al
        he_objone = 0
        for i in he_result:
            he_objone += al * (abs(i[0] - i[4]))
        he_objone += (he_result[-1][1] + he_result[-1][3])
        he_objtwo = 0
        for i in he_resulttwo:
            he_objtwo += al * (abs(i[0] - i[4]))
        he_objtwo += (he_resulttwo[-1][1] + he_resulttwo[-1][3])
        he_objthree = 0
        for i in he_resultthree:
            he_objthree += al * (abs(i[0] - i[4]))
        he_objthree += (he_resultthree[-1][1] + he_resultthree[-1][3])
        gb_result = gbexp.gb_solver(variables)
        compare_resultone[al] += ((he_objone - gb_result['Obj'])/gb_result['Obj'])
        compare_resultotwo[al] += ((he_objtwo - gb_result['Obj'])/gb_result['Obj'])
        compare_resultothree[al] += ((he_objthree - gb_result['Obj'])/gb_result['Obj'])
        
    #he_end = time.time()
    
    # he_time = he_end - he_strat
    #  gb_result = gbexp.gb_solver(variables)
    #print(he_result)
    #print('----------------------------------实验结果-------------------------------------')
    #print(he_obj)
    #print(he_time)
    #print(gb_result['Obj'])
    #print(gb_result['Runtime'])
    #compare_result.append([he_obj, gb_result['Obj']])
    #compare_time.append([he_time, gb_result['Runtime']])
for i in beixuan:
    compare_resultone[i] /= 10
    compare_resultotwo[i] /= 10
    compare_resultothree[i] /= 10
print(compare_resultone)
print(compare_resultotwo)
print(compare_resultothree)
