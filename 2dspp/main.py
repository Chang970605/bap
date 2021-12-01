from gurobipy import *

try:

    # Create a new model
    m = Model("sspwp")

    # Create variables
    # 参数
    N = 3      # 箱子数目
    W = 10     # 容器宽
    M = 100000 # 很大的数
    alpha = 0  # 惩罚系数
    w = {}     # 箱子宽
    h = {}     # 箱子高
    p = {}     # 箱子偏好位置
    for i in range(1, N + 1):
        w[i] = 2
        h[i] = 4
        p[i] = 1
    
    # 构建指标集
    item_list = [i for i in range(1, N + 1)]
    interactive_item_list = [(i, j) for i in range(1, N + 1) for j in range(1, N + 1) if i != j]
    
    # 决策变量
    d = m.addVars(interactive_item_list, vtype= GRB.BINARY, name = "d")
    l = m.addVars(interactive_item_list, vtype= GRB.BINARY, name = "l")
    x = m.addVars(item_list, vtype= GRB.CONTINUOUS, name = "x")
    y = m.addVars(item_list, vtype= GRB.CONTINUOUS, name = "y")      #左上角坐标
    h_max = m.addVar(vtype = GRB.CONTINUOUS, name = "h_max")
    px = m.addVars(item_list, vtype= GRB.CONTINUOUS, name = "px")
    # 带有广义约束的决策变量
    m.addGenConstrMax(h_max, [y[i] for i in item_list], name = "max_height")
    m.addGenConstrAbs(px[1], x[1] - p[1], "px1")
    # Set objective
    

    # Add constraint: x + 2 y + 3 z <= 4
    
    # Add constraint: x + y >= 1
    
    
    m.update()
    m.write('ssp.lp')
    '''
    m.optimize()

    for v in m.getVars():
        print(v.varName, v.x)

    print('Obj:', m.objVal)
    '''
except GurobiError:
    print('Error reported')
