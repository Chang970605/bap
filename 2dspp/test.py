import ha
import random
import gbexp
# x,y,w,h
p = [[0, 0, 0, 0],[0.3,0,0.3,4],[0.7,0,0.3,5],[0,0,0.3,6],[0.3,4,0.3,4],[0.75,5,0.25,4],[0,6,0.25,4]]
w = 0.3
h = 3
W = 1
# print(ha.find_position(p,w,h,W))
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
ww = list(w.values())[::-1]
hh = list(h.values())[::-1]
variables = {}
variables['N'] = 10
variables['W'] = 20
variables['w'] = w
variables['h'] = h
for j in range(1, 11):
    p[j] = random.randint(0, 20 - w[j])
variables['alpha'] = 3
variables['p'] = p
pp = list(p.values())[::-1]
he_result = ha.ffd(ww, hh, 20, pp)
he_obj = 0
for i in he_result:
    he_obj += abs(i[0] - i[4])
he_obj += (he_result[-1][1] + he_result[-1][3])
gb_result = gbexp.gb_solver(variables)
print(he_result)
print('----------------------------------实验结果-------------------------------------')
print(he_obj)
print(gb_result['Obj'])


