from gurobipy import *
import matplotlib.pyplot as plt
import random

def gb_solver(variables_dict):
    """
    使用gurobi解决带偏好的装箱问题，输入为字典，输出字典
    variables_dict: 需要包含以下几个参数
                    N:箱子数量
                    W:容器宽
                    alpha:惩罚系数
                    w: 箱子宽 dict like { w[1]: , w[2]:}
                    h: 箱子高 dict
                    p: 偏好位置 dict
    """
    try:
        # Create a new model
        m = Model("sspwp")
        # Create variables
        # 参数
        N = variables_dict['N']      # 箱子数目
        W = variables_dict['W']     # 容器宽
        M = 1000 # 很大的数
        alpha = variables_dict['alpha']  # 惩罚系数
        w = variables_dict['w']     # 箱子宽
        h = variables_dict['h']     # 箱子高
        p = variables_dict['p']     # 箱子偏好位置
        
        # 构建指标集
        item_list = [i for i in range(1, N + 1)]
        interactive_item_list = [(i, j) for i in range(1, N + 1) for j in range(1, N + 1) if i != j]
        
        # 决策变量
        d = m.addVars(interactive_item_list, vtype= GRB.BINARY, name = "d")
        l = m.addVars(interactive_item_list, vtype= GRB.BINARY, name = "l")
        x = m.addVars(item_list, vtype= GRB.INTEGER, name = "x")
        y = m.addVars(item_list, vtype= GRB.INTEGER, name = "y")      
        h_max = m.addVar(vtype = GRB.INTEGER, name = "h_max")
        px = m.addVars(item_list, lb = -500, vtype= GRB.INTEGER, name = "px")  # 算上偏移的x px = x - p 后面要加入约束
        yh = m.addVars(item_list, vtype= GRB.INTEGER, name = "yh")   # 算上高度的y yh = y + h 后面要加入约束
        pxf = m.addVars(item_list, vtype= GRB.INTEGER, name = "pxf") # 带绝对值的px
        
        # 带有广义约束的决策变量
        m.addGenConstrMax(h_max, [yh[i] for i in item_list], name = "max_height")
        for i in item_list:
            m.addGenConstrAbs(pxf[i], px[i], "abspx" + str(i))
        
        # Set objective
        m.setObjective(h_max + alpha * sum(pxf[i] for i in item_list), GRB.MINIMIZE)  # alpha * (sum(pxf[i] for i in item_list)
        # pxf = abs(x[i] - p[i])
        # Add constraint:
        for i,j in interactive_item_list:
            m.addConstr(y[i] - y[j] + h[i] <= (1 - d[i, j]) * M, "c0" + str(i) + str(j))
            
        for i,j in interactive_item_list:
            m.addConstr(x[i] - x[j] + w[i] <= (1 - l[i, j]) * M, "c1" + str(i) + str(j))
        
        for i,j in interactive_item_list:
            if i < j:
                m.addConstr(l[i, j] + l[j, i] <= 1, "c2" + str(i) + str(j))
                m.addConstr(d[i, j] + d[j, i] <= 1, "c3" + str(i) + str(j))
                m.addConstr(l[i, j] + l[j, i] + d[j, i] + d[i, j] >= 1, "c4" + str(i) + str(j))
        
        for i in item_list:
            m.addConstr(x[i] <= W - w[i], "x0" + str(i))
            m.addConstr(x[i] >= 0, "x1" + str(i))
            m.addConstr(y[i] >= 0, "y0" + str(i))
            m.addConstr(px[i] == x[i] - p[i], "px0" + str(i))
            m.addConstr(yh[i] == y[i] + h[i], "x0" + str(i))
        
        m.setParam("outputflag",0)
        m.Params.TimeLimit = 180
        m.update()
        m.write('ssp.lp')
        # m.setParam("MIPGap", 10**(-1))
        # 开始优化
        m.optimize()
        result =  {}  #保存结果
        for v in m.getVars():
            result[v.varName] = v.x

        result['Obj'] = m.objVal
        result['Runtime'] = m.Runtime
        
        pcount = 0
        for i in range(1, N + 1):
            pcount += abs(result['x[' + str(i) + ']'] - p[i])
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
    '''
    w[11], h[11] = 3, 2
    w[12], h[12] = 4, 2
    w[13], h[13] = 3, 4
    w[14], h[14] = 4, 4
    w[15], h[15] = 9, 2 
    w[16], h[16] = 11, 2
    '''
    
    variables = {}
    variables['N'] = 10
    variables['W'] = 20
    variables['w'] = w
    variables['h'] = h
    
    
    
    # ans = {}
    # p_ans = {}
    for j in range(1, 11):
        p[j] = random.randint(0, 20 - w[j])
    p = {1: 10, 2: 5, 3: 8, 4: 2, 5: 10, 6: 8, 7: 6, 8: 2, 9: 8, 10: 10}
    variables['alpha'] = 3
    variables['p'] = p
    result = gb_solver(variables)
    print(result)

    '''
    # 图2.4
    time = []
    punish = []
    ans = []
    time = []
    i = 0
    while i <= 4:
        print('--------------------i=' + str(i) + '---------------------')
        variables['alpha'] = i
        result = gb_solver(variables)
        punish.append(result['pcount'])
        ans.append(result['Obj'])
        i += 0.05
        time.append(result['Runtime'])
    print(ans)
    print(punish)
    print(p)
    print(time)
    '''
    '''
    ans = {}
    p_ans = {}
    for k in range(1):
        res = []
        variables['p'] = p
        i = 0
        while i <= 6:
            print('-------------------------------------------------开始' + str(i))    
            variables['alpha'] = i
            result = gb_solver(variables)
            res.append(result['pcount'])
            i += 0.1
        ans[k] = res
        pp = p.copy()
        p_ans[k] = pp
    print(ans)
    
    with open('exp1_1.txt', 'w') as f:
        for key, value in ans.items():
            f.write(str(key))
            f.write(': ')
            f.write(str(value))
            f.write('\n')
    with open('exp1_2.txt', 'w') as f:
        for key, value in p_ans.items():
            f.write(str(key))
            f.write(': ')
            f.write(str(value))
            f.write('\n')
    '''