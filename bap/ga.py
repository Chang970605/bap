import copy
# 编写ga
# 一些变量 B为船数, 
def translate(DNA, N, V, alpha, l, L, tide, B, a, p, c, Q, q_min, q_max):
    '''
    解码函数，最重要的函数
    dna: [[] * B]
    '''
    result = [] # 保存最终答案
    qiaoji_result = []
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
                    tmpp_ans.append([tmp_x, tmp_y + 1, tmp_l, tmp_h, tmp_leave, tmp_index, tmp_p])
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
                    ttmp_ans.append([tmp_p, tmp_y + 1, tmp_l, tmp_h, tmp_leave, tmp_index, tmp_p])
                    ttmp_ans[0] += tmp_cost
                    tmp_beam_ans.append(ttmp_ans)
            tmp_beam_ans.sort(key = lambda x : x[0])
            beam_ans = tmp_beam_ans[:10]
        tmp_result = beam_ans[0]
        if len(tmp_result) != B + 1:
            continue
        # result.append(tmp_result)  这块先不存，桥机分配成功了再存

        # result里全是[[cost, [x,y,l,h]]]
        # 接下来分桥机
        # 处理 tmp_result B + 1个
        working_nums = [0] * (2 * N * V  + 1) # 统计每个时间段有多少 方便下标统一
        working_ship = [[] for _ in range(2 * N * V + 1)]
        for i in range(1, len(tmp_result)):
            tmp_tstart = tmp_result[i][1]
            tmp_end = tmp_result[i][1] + tmp_result[i][3]
            for t in range(tmp_tstart, tmp_end):
                working_nums[t] += 1
                working_ship[t].append(i) # 此时的i为tmp_result的索引，并非船的编号
        # 已经统计完毕,开始分配桥机
        remain_work = {}
        remain_time = {}
        remain_average  = {}
        qiaoji_plan = {}
        berth_qiaoji = False
        for t in range(1, 2 * N * V + 1):
            work_sum = 0
            del_working_ship = []
            for i in working_ship[t]:
                tmp_tstart = tmp_result[i][1]
                tmp_shipindex = tmp_result[i][5]
                if t == tmp_tstart:
                    remain_time[i] = tmp_result[i][3] # 后面要减
                    remain_work[i] = c[tmp_shipindex]
                    qiaoji_plan[i] = []
                if remain_work[i] == 0:
                    del_working_ship.append(i)
                    continue
                remain_average[i] = remain_work[i] / remain_time[i]
                work_sum += remain_average[i]
            left_qiaoji = Q # 后面用来减
            for i in del_working_ship:
                working_ship[t].remove(i)
            for i in working_ship[t]:
                if remain_work[i] == 0:
                    continue
                tmp_shipindex = tmp_result[i][5]
                tmp_qiaoji = int(Q * (remain_average[i] / work_sum))
                if tmp_qiaoji < q_min[tmp_shipindex]:
                    tmp_qiaoji = q_min[tmp_shipindex]
                elif tmp_qiaoji > q_max[tmp_shipindex]:
                    tmp_qiaoji = q_max[tmp_shipindex]
                qiaoji_plan[i].append(tmp_qiaoji)
                left_qiaoji -= tmp_qiaoji
            if left_qiaoji > 0:
                # 还有剩余，分给第一个？
                for i in working_ship[t]:
                    tmp_shipindex = tmp_result[i][5]
                    if qiaoji_plan[i][-1] < q_max[tmp_shipindex]:
                        cha = q_max[tmp_shipindex] - qiaoji_plan[i][-1]
                        if cha >= left_qiaoji:
                            qiaoji_plan[i][-1] += left_qiaoji
                            left_qiaoji == 0
                            break
                        else:
                            # cha < left
                            qiaoji_plan[i][-1] += cha
                            left_qiaoji -= cha
            if left_qiaoji < 0:
                for i in working_ship[t]:
                    tmp_shipindex = tmp_result[i][5]
                    if qiaoji_plan[i][-1] > q_min[tmp_shipindex]:
                        cha = qiaoji_plan[i][-1] - q_min[tmp_shipindex]
                        if cha >= abs(left_qiaoji):
                            qiaoji_plan[i][-1] -= left_qiaoji
                            left_qiaoji == 0
                            break
                        else:
                            # cha < left
                            qiaoji_plan[i][-1] -= cha
                            left_qiaoji += cha
            if left_qiaoji >= 0:
                for i in working_ship[t]:
                    if qiaoji_plan[i][-1] >= remain_work[i]:
                        qiaoji_plan[i][-1] = remain_work[i]
                        remain_work[i] -= qiaoji_plan[i][-1]
                        # 重新确定 x,y,l,h,后面需要重新算一下哈
                        tmp_result[i][3] = t - tmp_result[i][1] + 1
                    else:
                        remain_work[i] -= qiaoji_plan[i][-1]
                        remain_time[i] -= 1
                        if remain_time[i] == 0:
                            remain_time[i] += 1
                            tmp_result[i][3] += 1
                            working_nums[t + 1] +=1
                            working_ship[t + 1].append(i)
                berth_qiaoji = True
            for i in working_ship[t]:
                tmp_shipindex = tmp_result[i][5]
                if qiaoji_plan[i][-1] > q_max[tmp_shipindex] or qiaoji_plan[i][-1] < q_min[tmp_shipindex]:
                    berth_qiaoji == False
            if not berth_qiaoji:
                break
        # tmp_result = tmp_result[1:]
        for i in range(1, len(tmp_result)):
            tmp_start = tmp_result[i][1]
            tmp_leave = tmp_start + tmp_result[i][3]
            tmp_index = tmp_result[i][5]
            tmp_result[i][4] = into_shipchannel(tmp_leave, N, V, tide, tmp_index)
            if tmp_result[i][4] > 2 * N * V:
                berth_qiaoji = False
        for i in range(1, len(tmp_result)):
            tmp_ans = tmp_result[:i]
            tmp_x = tmp_result[i][0]
            tmp_ts = tmp_result[i][1]
            tmp_l = tmp_result[i][2]
            tmp_h = tmp_result[i][3]
            if not can_berth(tmp_ans, tmp_x, tmp_ts, tmp_l, tmp_h, N, V):
                berth_qiaoji = False
        if berth_qiaoji:
            result.append([tmp_result[1:], qiaoji_plan])
        else:
            result.append([])
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