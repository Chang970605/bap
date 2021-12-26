import copy
# 编写ga
# 一些变量 B为船数, 
def translate(DNA, N, V, alpha, l, L, tide, B, a, p):
    '''
    解码函数，最重要的函数
    dna: [[] * B]
    '''
    result = [] # 保存最终答案
    for dna_tmp in DNA:
        # 对每一个基因进行解码 dna_tmp list [3 * B] 船号 泊位位置 预计工作时间
        # 从此开始进行解码
        beam_ans = [[0]] # 保存每一个编码的所有答案 [[cost, [x,y,l,h], [x,y,l,h]]]
        for i in range(B):
            tmp_index = dna_tmp[i] # 船号
            tmp_l = l[tmp_index] # 船宽
            tmp_x = dna_tmp[i + B] # 位置
            tmp_h = dna_tmp[i + 2 * B] # 预计时间
            tmp_a = a[tmp_index]
            tmp_p = p[tmp_index] # 偏好位置 做beam_search
            tmp_beam_ans = [] # 保存新的
            for tmp_ans in beam_ans:
                # tmp_ans [cost, [x, y, l, h],[]...]
                # 每一个都需要考虑两个
                # 首先确定y 起始时间
                # 首先处理 tmp_x
                tmpp_ans = copy.deepcopy(tmp_ans)
                breath = False
                tmp_y  = tmp_a
                while not breath:
                    tmp_y = into_shipchannel(tmp_y, N, V, tide, tmp_index) # 得到最近的可能时间
                    if tmp_y > 2 * V * N: # 此时这种方案不行了
                        break # 此时breath = False
                    tmp_ts = tmp_y + 1 # 进港需要时间
                    if can_berth(tmp_ans, tmp_x, tmp_ts, tmp_l, tmp_h, N, V):
                        breath = True
                        tmp_leave = tmp_y + 1 + tmp_h
                        tmp_leave = into_shipchannel(tmp_leave, N, V, tide, tmp_index)
                        if tmp_leave > 2 * V * N:
                            breath = False
                            tmp_y += 1
                    else:
                        tmp_y += 1
                # 需要计算cost
                if breath:
                    tmp_leave = tmp_y + 1 + tmp_h
                    tmp_leave = into_shipchannel(tmp_leave, N, V, tide, tmp_index)
                    tmp_cost = (tmp_leave - tmp_a) + alpha * abs(tmp_x - tmp_p) 
                    tmpp_ans.append([tmp_x, tmp_y + 1, tmp_l, tmp_h])
                    tmpp_ans[0] += tmp_cost
                    tmp_beam_ans.append(tmpp_ans)
                # 开始考虑tmp_p
                ttmp_ans = copy.deepcopy(tmp_ans)
                breath = False
                tmp_y  = tmp_a
                while not breath:
                    tmp_y = into_shipchannel(tmp_y, N, V, tide, tmp_index) # 得到最近的可能时间
                    if tmp_y > 2 * V * N: # 此时这种方案不行了
                        break # 此时breath = False
                    tmp_ts = tmp_y + 1 # 进港需要时间
                    if can_berth(tmp_ans, tmp_p, tmp_ts, tmp_l, tmp_h, N, V):
                        breath = True
                        tmp_leave = tmp_y + 1 + tmp_h
                        tmp_leave = into_shipchannel(tmp_leave, N, V, tide, tmp_index)
                        if tmp_leave > 2 * V * N:
                            breath = False
                            tmp_y += 1
                    else:
                        tmp_y += 1
                if breath:
                    tmp_leave = tmp_y + 1 + tmp_h
                    tmp_leave = into_shipchannel(tmp_leave, N, V, tide, tmp_index)
                    tmp_cost = tmp_leave - tmp_a
                    ttmp_ans.append([tmp_p, tmp_y + 1, tmp_l, tmp_h])
                    ttmp_ans[0] += tmp_cost
                    tmp_beam_ans.append(ttmp_ans)
            tmp_beam_ans.sort(key = lambda x : x[0])
            beam_ans = tmp_beam_ans[:10]
        tmp_result = beam_ans[0]
        result.append(tmp_result)
    return result

def can_berth(ans, x, y, l, h, N, V):
    '''
    判断是否可以停靠，即判断是否有重叠，要判断作业时间是否超过总时长
    ans: list like [cost, [x, y, l, h],...]
    x: 停靠位置
    y: 开始时间
    l: 船的宽度
    h: 船的作业时间
    '''
    if len(ans) == 1:
        if l + y <= 2 * N * V:
            return True
        else:
            return False
    for i in range(1, len(ans)):
        tmp = ans[i]
        # tmp like [x,y,l,h]
        if tmp[0] + tmp[2] - 1< x or tmp[0] > x + l - 1:
            continue
        else:
            # 此时x有重叠
            if tmp[1] > y + h - 1 or tmp[1] + tmp[3] - 1< y:
                continue
            else:
                return False
    if l + y <= 2 * N * V:
        return True
    else:
        return False


def into_shipchannel(t, N, V, tide, i):
    '''
    用来确定是否能进入航道，主要是水位影响，若能，直接返回t，若不能，返回最近的一次，并不考虑重叠
    t: 为此时的时间，最开始用a
    N: 几个轮次潮汐
    V: 一个水位的持续时间
    tide: 受影响的船只集合
    i: 船号
    '''
    c = (t - 1) // (2 * V)
    if c >= N:
        return 2 * N * V + 1  # 此时加一个判断，在后面，这个解码就不能用了
    else: # 此时 c < N
        if i not in tide:
            return t
        else: # 此时 i in tide
            t_tmp = t % (2 * V)
            if t_tmp >= 1 and t_tmp <= V:
                return t
            else:
                return (c + 1) * (2 * V) + 1

def git_fitness(x):
    '''
    适应度评估函数
    '''
    pass

def select(x):
    '''
    选择函数
    '''
    pass

def crossover(x):
    '''
    交叉函数
    '''
    pass

def mutation(x):
    '''
    变异函数
    '''
    pass

def evolution(x):
    '''
    进化函数
    '''