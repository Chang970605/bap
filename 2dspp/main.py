from gurobipy import *

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
        M = 100000 # 很大的数
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
        x = m.addVars(item_list, vtype= GRB.CONTINUOUS, name = "x")
        y = m.addVars(item_list, vtype= GRB.CONTINUOUS, name = "y")      
        h_max = m.addVar(vtype = GRB.CONTINUOUS, name = "h_max")
        px = m.addVars(item_list, vtype= GRB.CONTINUOUS, name = "px")  # 算上偏移的x px = x - p 后面要加入约束
        yh = m.addVars(item_list, vtype= GRB.CONTINUOUS, name = "yh")   # 算上高度的y yh = y + h 后面要加入约束
        pxf = m.addVars(item_list, vtype= GRB.CONTINUOUS, name = "pxf") # 带绝对值的px
        
        # 带有广义约束的决策变量
        m.addGenConstrMax(h_max, [yh[i] for i in item_list], name = "max_height")
        for i in item_list:
            m.addGenConstrAbs(pxf[i], px[i], "abspx" + str(i))
        
        # Set objective
        m.setObjective(h_max + alpha * sum(pxf[i] for i in item_list), GRB.MINIMIZE)

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
        
        # m.update()
        # m.write('ssp.lp')
        
        # 开始优化
        m.optimize()
        result =  {}  #保存结果
        for v in m.getVars():
            result[v.varName] = v.x

        result['Obj'] = m.objVal
        result['Runtime'] = m.Runtime
        return result

    except GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')

if __name__ == "__main__":
    w = {}     # 箱子宽
    h = {}     # 箱子高
    p = {}     # 箱子偏好位置
    for i in range(1, 3 + 1):
        w[i] = 2
        h[i] = 4
        p[i] = 1 
    variables = {}
    variables['N'] = 3
    variables['W'] = 10
    variables['w'] = w
    variables['h'] = h
    variables['p'] = p
    variables['alpha'] = 0
    result = gb_solver(variables)
    print(result)