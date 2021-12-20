from gurobipy import *
import matplotlib.pyplot as plt
import random

def gb_solver(variables_dict):
    """
    使用gurobi解决带偏好的bap问题，输入为字典，输出字典
    variables_dict: 需要包含以下几个参数
                    B:船舶的总数目
                    N:一共多少个高水位
                    V:每一个高水位持续的时间
                    L:港口的宽度
                    alpha:惩罚系数
                    l: 船宽 dict like { w[1]: , w[2]:}
                    tide: list []
                    free: list
                    c: 工作量dict
                    q_max: dict 最多桥机数
                    q_min: dict 最少桥机数
                    p: dict 偏好位置
                    a: dict 到达时间
    """
    try:
        # Create a new model
        m = Model("bapwp")
        # Create variables
        # 参数
        B = variables_dict['B']      # 箱子数目
        N = variables_dict['N']    #一共多少个高水位
        V = variables_dict['V']    # 每一个高水位持续的时间
        L = variables_dict['L']     # 容器宽
        Q = variables_dict['Q']     # 容器的总数目
        M = 1000 # 很大的数 不能太大 否则会出精度问题
        alpha = variables_dict['alpha']  # 惩罚系数
        l = variables_dict['l']     # 箱子宽
        tide = variables_dict['tide'] # 受潮汐影响的 list
        free = variables_dict['free'] # 不受潮汐影响的下标 list
        c = variables_dict['c']     # 每个船的工作量
        q_max = variables_dict['q_max'] # 每个船的最多工作桥机数
        q_min = variables_dict['q_min'] # 每个船的最少工作桥机数
        p = variables_dict['p']     # 箱子偏好位置
        a = variables_dict['a']  # dict 船的到达时间
        
        
        # 构建指标集 后面约束要用的
        item_list = [i for i in range(1, B + 1)]
        item_tide_list = [i for i in tide]
        item_free_list = [i for i in free]
        interactive_item_list = [(i, j) for i in range(1, B + 1) for j in range(1, B + 1) if i != j]
        n_list = [i for i in range(1, N + 1)] # n的集合
        interactive_item_n_list = [(i, j) for i in range(1, B + 1) for j in range(1, N + 1)]
        interactive_item_t_list = [(i, j) for i in range(1, B + 1) for j in range(1, 2 * N * V + 1)]
        interactive_q_item_t_list = [(i, j, k) for i in range(1, Q + 1) for j in range(1, B + 1) for k in range(1, 2 * N * V + 1)]
        interactive_tideitem_n_list = [(i, j) for i in tide for j in range(1, N + 1)]
        # 决策变量
        ts = m.addVars(item_list, vtype= GRB.INTEGER, name = "ts") # 每个船的开始工作时间
        b = m.addVars(item_list, vtype= GRB.INTEGER, name = "b") # b_{i} 每个船i的停靠位置
        rou = m.addVars(item_list, vtype= GRB.INTEGER, name = "rou") # rou 每个船的工作时间
        ti = m.addVars(item_list, vtype= GRB.INTEGER, name = "ti") # 每个船进入航道的时间，与开始工作时间是强相关的
        to = m.addVars(item_list, vtype= GRB.INTEGER, name = "to") # 每个船驶出航道的时间，需要等到高水位
        te = m.addVars(item_list, vtype= GRB.INTEGER, name = "te") # 每个船结束工作的时间 time_end
        miu = m.addVars(interactive_item_n_list, vtype= GRB.BINARY, name = "miu")  # miu_{in} 船在第n个高水位进入
        v = m.addVars(interactive_item_n_list, vtype= GRB.BINARY, name = "v")  # v_{in} 船在第n个高水位驶出
        ceta = m.addVars(interactive_item_t_list, vtype= GRB.BINARY, name = "ceta") # ceta_{it} 船i在时刻t是否工作
        pai = m.addVars(interactive_item_t_list, vtype= GRB.BINARY, name = "pao") # pai_{it} 船i在时刻t是否为开始工作
        fei = m.addVars(interactive_item_t_list, vtype= GRB.BINARY, name = "fei") # fei_{it} 船i再时刻t是否结束工作
        hiu = m.addVars(interactive_q_item_t_list, vtype= GRB.BINARY, name = "hiu") # hiu_{qit}船机q在t时刻给船i工作

        d = m.addVars(interactive_item_list, vtype= GRB.BINARY, name = "d")
        left = m.addVars(interactive_item_list, vtype= GRB.BINARY, name = "left")
        # .     
        # h_max = m.addVar(vtype = GRB.INTEGER, name = "h_max")
        px = m.addVars(item_list, lb = -500, vtype= GRB.INTEGER, name = "px")  # 算上偏移的x px = x - p 后面要加入约束
        # yh = m.addVars(item_list, vtype= GRB.INTEGER, name = "yh")   # 算上高度的y yh = y + h 后面要加入约束
        pxf = m.addVars(item_list, vtype= GRB.INTEGER, name = "pxf") # 带绝对值的px
        
        # 带有广义约束的决策变量
        # m.addGenConstrMax(h_max, [yh[i] for i in item_list], name = "max_height")
        for i in item_list:
            m.addGenConstrAbs(pxf[i], px[i], "abspx" + str(i))
        
        # Set objective
        m.setObjective(sum((to[i] - a[i]) for i in item_list) + alpha * sum(pxf[i] for i in item_list), GRB.MINIMIZE)  # alpha * (sum(pxf[i] for i in item_list)
        # pxf = abs(x[i] - p[i])
        
        # Add constraint:
        for i in item_list:
            m.addConstr(ti[i] >= a[i], "c0" + str(i))
            m.addConstr(ts[i] == ti[i] + 1, "c1" + str(i))
            m.addConstr(to[i] >= te[i], "c2" + str(i))
            m.addConstr(te[i] - ts[i] == sum(ceta[i, j] for j in range(1, 2 * N * V + 1)), "c3" + str(i))
            m.addConstr(1 == sum(pai[i, j] for j in range(1, 2 * N * V + 1)), "c77" + str(i))
            m.addConstr(1 == sum(fei[i, j] for j in range(1, 2 * N * V + 1)), "c78" + str(i))
            m.addConstr(ts[i] == sum(j * pai[i, j] for j in range(1, 2 * N * V + 1)), "c4" + str(i))  # 后续关注一下约束对不对
            m.addConstr(te[i] == sum(j * fei[i, j] for j in range(1, 2 * N * V + 1)), "c5" + str(i))
            m.addConstr(rou[i] == sum(ceta[i, j] for j in range(1, 2 * N * V + 1)), "c6" + str(i))
        
        for i in item_tide_list:
            m.addConstr(sum(miu[i, j] for j in n_list) == 1, "b0" + str(i))
            m.addConstr(sum(v[i, j] for j in n_list) == 1, "b1" + str(i))
        
        for i, j in interactive_tideitem_n_list:
            m.addConstr(ti[i] >= 2 * (j - 1) * V + 1 - M * (1 - miu[i, j]), "a0" + str(i) + str(j))
            m.addConstr(ti[i] <= (2 * j - 1) * V + M * (1 - miu[i, j]), "a1" + str(i) + str(j))
            m.addConstr(to[i] >= 2 * (j - 1) * V + 1 - M * (1 - v[i, j]), "a2" + str(i) + str(j))
            m.addConstr(to[i] <= (2 * j - 1) * V + M * (1 - v[i, j]), "a3" + str(i) + str(j))
        
        for i in item_list:
            for j in range(2, 2 * N * V + 1):
                m.addConstr(sum(ceta[i, t] for t in range(1, j)) <= M * (1 - pai[i, j]), "d00" + str(i) + str(32323) + str(j))

        for i in item_list:
            for j in range(1, 2 * N * V + 1):
                m.addConstr(sum(ceta[i, t] for t in range(j, 2 * N * V + 1)) <= M * (1 - fei[i, j]), "d1" + str(i) + str(j))

        for i, j in interactive_item_list:
            m.addConstr(b[i] - b[j] + l[i] <= (1 - left[i, j]) * L, "e0" + str(i) + str(j))
            m.addConstr(ts[i] - ts[j] + rou[i] <= (1 - d[i, j]) * M, "e1" + str(i) + str(j))
        
        for i,j in interactive_item_list:
            if i < j:
                m.addConstr(left[i, j] + left[j, i] <= 1, "e2" + str(i) + str(j))
                m.addConstr(d[i, j] + d[j, i] <= 1, "e3" + str(i) + str(j))
                m.addConstr(left[i, j] + left[j, i] + d[j, i] + d[i, j] >= 1, "e4" + str(i) + str(j))
        
        for t in range(1, 2 * N * V + 1):
            m.addConstr(sum(sum(hiu[q, i, t] for q in range(1, Q + 1)) for i in range(1, B + 1)) <= Q, "h0" + str(t))
            for q in range(1, Q + 1):
                m.addConstr(sum(hiu[q, i, t] for i in item_list) <= 1, "h2" + str(t) + str(q))
            for i in item_list:
                m.addConstr(sum(hiu[q, i, t] for q in range(1, Q + 1)) <= q_max[i] + M * (1 - ceta[i, t]), "h3" + str(t) + str(i))
                m.addConstr(sum(hiu[q, i, t] for q in range(1, Q + 1)) >= q_min[i] - M * (1 - ceta[i, t]), "h4" + str(t) + str(i))
                m.addConstr(sum(hiu[q, i, t] for q in range(1, Q + 1)) <= M * ceta[i, t], "h5" + str(t) + str(i))
                for q in range(2, Q + 1):
                    for qq in range(q + 1, Q + 1):
                        m.addConstr(hiu[qq, i, t] + hiu[q - 1, i, t] - hiu[q, i, t] <= 1, "h6" + str(i) + str(t) + str(q) + str(qq))
            for i , ii in interactive_item_list:
                for q in range(1, Q + 1):
                    for qq in range(1, Q + 1):
                        if q != qq:
                            m.addConstr(q <= qq + M * (3 - hiu[q, i, t] - hiu[qq, ii ,t] - left[i, ii]) + 1, "h7" + str(t) + str(q) + str(qq) + str(i) + str(ii))
        

        for i in item_list:
            m.addConstr(sum(sum(hiu[q, i, t] for q in range(1, Q + 1)) for t in range(1, 2 * N * V + 1)) == c[i], "h1" + str(i))
            for t in range(1, 2 * N * V + 1):
                for tt in range(1, 2 * N * V + 1):
                    if t != tt:
                        m.addConstr(sum(hiu[q, i, t] for q in range(1, Q + 1)) - sum(hiu[q, i, tt] for q in range(1, Q + 1)) >= (-1) * M * (2 - ceta[i, t] - ceta[i, tt]) - 1, "h555" + str(t) + str(i) + str(tt))

        for i in item_list:
            m.addConstr(b[i] <= L - l[i] + 1, "x0" + str(i))
            m.addConstr(b[i] >= 1, "x1" + str(i))
            m.addConstr(ti[i] >= 1, "x2" + str(i))
            # m.addConstr(ts[i] >= 0, "y0" + str(i))
            m.addConstr(to[i] <= 2 * N * V, "t0" + str(i))
            m.addConstr(px[i] == b[i] - p[i], "px0" + str(i))
            # m.addConstr(yh[i] == y[i] + h[i], "x0" + str(i))
        
        m.update()
        m.write('ssp.lp')
        # m.setParam("MIPGap", 1)
        # 开始优化
        m.optimize()
        result =  {}  #保存结果
        for v in m.getVars():
            result[v.varName] = v.x

        result['Obj'] = m.objVal
        result['Runtime'] = m.Runtime
        
        pcount = 0
        for i in range(1, N + 1):
            pcount += abs(result['b[' + str(i) + ']'] - p[i])
        result['pcount'] = pcount
        return result

    except GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')

def sketch_map(W, w, h, x, y, p, name):
    """
    画结果示意图
    W: 容器的宽度
    w: 数组，为每个箱子的宽度
    h: 数组，为每个箱子的高度
    p: 数组，为每个箱子的偏好位置
    x: 数组，为每个箱子左下角x坐标
    y: 数组，为每个箱子左下角y坐标
    name: str，图片保存名字
    """
    # 先确定x,y轴范围
    y_label_range = 1.6 * max([i + j for i, j in zip(y, h)])
    x_label_range = W
    
    # 开始做图
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    #建立矩形
    for i in range(len(w)):
        rect = plt.Rectangle(
                (x[i], y[i]),  # (x,y)矩形左下角
                w[i],          # width长
                h[i],          # height宽
                color='maroon', 
                alpha=0.5)
        ax.add_patch(rect)
        ax.text(x[i] + (w[i] / 2), y[i] + (h[i] / 2),
                '{:s} {:.3f}'.format('sss', 11),
                bbox=dict(facecolor='blue', alpha=0.5),
                fontsize=14, color='white')
    # 建立图
    plt.xlim(0, x_label_range)
    plt.ylim(0, y_label_range)
    plt.show()
    plt.savefig(name + ".png")

if __name__ == "__main__":
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
    variables = {}
    variables['B'] = 7
    variables['L'] = 8
    variables['Q'] = 7
    variables['N'] = 3
    variables['V'] = 6
    variables['q_max'] = q_max
    variables['q_min'] = q_min
    variables['a'] = a
    variables['l'] = l
    variables['c'] = c
    variables['tide'] = tide
    variables['free'] = free
    variables['alpha'] = 0
    variables['p'] = p
    result = gb_solver(variables)
    print(result)
