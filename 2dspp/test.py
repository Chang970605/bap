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
beixuan = [0,0.1,0.2,0,3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9,5]
compare_resultone = {}
compare_resultotwo = {}
compare_resultothree = {}
comapre_resultofour = {}
for i in beixuan:
    compare_resultone[i] = 0
    compare_resultotwo[i] = 0
    compare_resultothree[i] = 0
    comapre_resultofour[i] = 0
for kk in range(1000):
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
    n = 20
    ww = []
    hh = []
    for _ in range(n):
        ww.append(random.randint(5, 15))
        hh.append(random.randint(30, 70))
    ww.sort()
    hh.sort()
    ww = ww[::-1]
    hh = hh[::-1]
    # ww = list(w.values())[::-1]
    # hh = list(h.values())[::-1]
    for j in range(1, n + 1):
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
    
    # print(he_result)
    # print(he_resulttwo)
    for alp in beixuan:
        he_resultfour = ha.ffd_beamsearch(ww, hh, 20, pp, alp)
        tmp_one = 0
        tmp_two = 0
        tmp_three = 0
        tmp_four = 0
        for i in range(len(he_result)):
            tmp_one += alp * abs(he_result[i][0] - he_result[i][4])
            tmp_two += alp * abs(he_resulttwo[i][0] - he_resulttwo[i][4])
            tmp_three += alp * abs(he_resultthree[i][0] - he_resultthree[i][4])
            tmp_four += alp * abs(he_resultfour[i][0] - he_resultfour[i][4])
        
        tmp_one += he_result[-1][1] + he_result[-1][3]
        tmp_two += he_resulttwo[-1][1] + he_resulttwo[-1][3]
        tmp_three += he_resultthree[-1][1] + he_resultthree[-1][3]
        tmp_four += he_resultfour[-1][1] + he_resultfour[-1][3] 
        tmpppp = min(tmp_one, tmp_two, tmp_three, tmp_four)
        if tmp_one == tmpppp:
            compare_resultone[alp] += 1
        if tmp_three == tmpppp:
            compare_resultothree[alp] += 1
        if tmp_two == tmpppp:
            compare_resultotwo[alp] += 1
        if tmp_four == tmpppp:
            comapre_resultofour[alp] += 1
    '''
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
        # gb_result = gbexp.gb_solver(variables)
        tmp_result = min(he_objone, he_objtwo, he_objthree)
        if tmp_result == he_objone:
            compare_resultone[al] += 1
        elif tmp_result == he_objtwo:
            compare_resultotwo[al] += 1
        else:
            compare_resultothree[al] += 1
        
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
    '''
#for i in beixuan:
#    compare_resultone[i] /= 10
#    compare_resultotwo[i] /= 10
#    compare_resultothree[i] /= 10
print(compare_resultone)
print(compare_resultotwo)
print(compare_resultothree)
print(comapre_resultofour)