import ha
import random
import gbexp
import time
import copy
def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    with open(filename, 'w') as f:
        for key, value in data.items():
            f.write(str(key))
            f.write(': ')
            f.write(str(value))
            f.write('\n')
# x,y,w,h
# p = [[0, 0, 0, 0],[0.3,0,0.3,4],[0.7,0,0.3,5],[0,0,0.3,6],[0.3,4,0.3,4],[0.75,5,0.25,4],[0,6,0.25,4]]
# w = 0.3
# h = 3
# W = 1
# print(ha.find_position(p,w,h,W))
beixuan = [0,0.1,0.2,0,3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3]
al_exp = [0, 0.1, 0.2, 0.3, 0.4, 0.5,1,1.5,2,3]
resone = {}
restwo = {}
resthree = {}
resfour = {}
resgurobi = {}
restimeone = {}
restimetwo = {}
restimethree = {}
restimefour = {}
restimegurobi = {}
for alp in beixuan:
    resone[alp] = []
    restwo[alp] = []
    resthree[alp] = []
    resfour[alp] = []
    resgurobi[alp] = []
    restimeone[alp] = []
    restimetwo[alp] = []
    restimethree[alp] = []
    restimefour[alp] = []
    restimegurobi[alp] = []

for n in [15]:
    print('------------------------------n=' + str(n))
    for k in range(10): #试验次数
        print('-----------------------' + str(n) + '第几次' + str(k))
        w = {}
        h = {}
        p = {}
        n_small = n // 3
        n_mid = n //3
        n_large = n - n_small - n_mid
        tmp_w = []
        tmp_h = []
        for i in range(1, n_small + 1):
            tmp_w.append(random.randint(1, 3))
            tmp_h.append(random.randint(3, 6))
        tmp_w.sort()
        tmp_h.sort()
        #ww = ww[::-1]
        #hh = hh[::-1]
        for i in range(1, n_small + 1):
            w[i] = tmp_w[i - 1]
            h[i] = tmp_h[i - 1]
            p[i] = random.randint(0, 20 - w[i])
        tmp_w = []
        tmp_h = []
        for i in range(n_small + 1, n_small + n_mid + 1):
            tmp_w.append(random.randint(4, 6))
            tmp_h.append(random.randint(7, 10))
        tmp_w.sort()
        tmp_h.sort()
        #ww = ww[::-1]
        #hh = hh[::-1]
        for i in range(n_small + 1, n_small + n_mid + 1):
            w[i] = tmp_w[i - n_small - 1]
            h[i] = tmp_h[i - n_small - 1]
            p[i] = random.randint(0, 20 - w[i])
        tmp_w = []
        tmp_h = []
        for i in range(n_small + n_mid + 1, n + 1):
            tmp_w.append(random.randint(7, 9))
            tmp_h.append(random.randint(11, 14))
        tmp_w.sort()
        tmp_h.sort()
        #ww = ww[::-1]
        #hh = hh[::-1]
        for i in range(n_small + n_mid + 1, n + 1):
            w[i] = tmp_w[i - n_small - n_mid - 1]
            h[i] = tmp_h[i - n_small - n_mid - 1]
            p[i] = random.randint(0, 20 - w[i])
        ww = list(w.values())
        hh = list(h.values())
        pp = list(p.values())
        ww = ww[::-1]
        pp = pp[::-1]
        hh = hh[::-1]
        variables = {}
        variables['N'] = n
        variables['W'] = 20
        variables['w'] = w
        variables['h'] = h
        variables['p'] = p
        for alp in beixuan:
            print('-----------' + str(alp))
            variables['alpha'] = alp
            result = gbexp.gb_solver(variables)
            gurobi_ans = result['Obj']
            restimegurobi[alp].append(result['Runtime'])
            resgurobi[alp].append(gurobi_ans)
            # print(restimegurobi)
            
            result_one, time_one = ha.ffd_withswap(copy.deepcopy(ww), copy.deepcopy(hh), 20,copy.deepcopy(pp), alp)
            result_two, time_two = ha.ffdtwo_withswap(copy.deepcopy(ww), copy.deepcopy(hh), 20,copy.deepcopy(pp), alp)
            result_three, time_three = ha.ffd_beamsearch_withswap(copy.deepcopy(ww), copy.deepcopy(hh), 20,copy.deepcopy(pp), alp)
            result_four, time_four = ha.ffd_beamsearch_withswap_new(copy.deepcopy(ww), copy.deepcopy(hh), 20,copy.deepcopy(pp), alp)
            resone[alp].append(result_one)
            restwo[alp].append(result_two)
            resthree[alp].append(result_three)
            resfour[alp].append(result_four)
            restimeone[alp].append(time_one)
            restimetwo[alp].append(time_two)
            restimethree[alp].append(time_three)
            restimefour[alp].append(time_four)
            print(resgurobi)
            print(restimegurobi)
            
            print(resone)
            print(restimeone)
            print(restwo)
            print(restimetwo)
            print(resthree)
            print(restimethree)
            print(resfour)
            print(restimefour)
# print(resone)
# print(restwo)
# print(restimeone)
# print(restimetwo)
print('--------------结果----------------')
print(restimegurobi)
print(resgurobi)
print(resone)
print(restimeone)
print(restwo)
print(restimetwo)
print(resthree)
print(restimethree)
print(resfour)
print(restimefour)
text_save('resgurobinew_4050.txt',resgurobi)
text_save('restimegurobinew_4050.txt',restimegurobi)
text_save('resonenew_4050.txt',resone)
text_save('restimeonenew_4050.txt',restimeone)
text_save('restwonew_4050.txt',restwo)
text_save('restimetwonew_4050.txt',restimetwo)
text_save('resthreenew_4050.txt',resthree)
text_save('restimethreenew_4050.txt',restimethree)
text_save('resfournew_4050.txt',resfour)
text_save('restimefournew_4050.txt',restimefour)

'''
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
    '''

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
    
#for i in beixuan:
#    compare_resultone[i] /= 10
#    compare_resultotwo[i] /= 10
#    compare_resultothree[i] /= 10
'''
print(compare_resultone)
print(compare_resultotwo)
print(compare_resultothree)
print(comapre_resultofour)
'''