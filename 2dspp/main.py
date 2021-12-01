from gurobipy import *

try:
    
    # Create a new model
    m = Model("sspwp")

    # Create variables
    # 参数
    N = 3     # 箱子数目
    W = 10    # 容器宽
    w = {}
    h = {}
    for i in range(1, N + 1):
        w[i] = 2
        h[i] = 4
    

    # 构建指标集
    item_list = [i for i in range(1, N + 1)]
    interactive_item_list = [(i, j) for i in range(1, N + 1) for j in range(1, N + 1) if i != j]
    
    # 决策变量
    d = m.addVars(interactive_item_list, vtype= GRB.BINARY, name = "d")
    l = m.addVars(interactive_item_list, vtype= GRB.BINARY, name = "l")
    x = m.addVars(item_list, vtype= GRB.CONTINUOUS, name = "x")
    y = m.addVars(item_list, vtype= GRB.CONTINUOUS, name = "y")
    
    # 参数
    



    # Set objective


    # Add constraint: x + 2 y + 3 z <= 4
    
    # Add constraint: x + y >= 1
    
    
    m.update()
    print(w[1])
    m.write('ssp.lp')
    '''
    m.optimize()

    for v in m.getVars():
        print(v.varName, v.x)

    print('Obj:', m.objVal)
    '''
except GurobiError:
    print('Error reported')
