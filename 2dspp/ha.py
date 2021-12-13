import copy

def ffd(w, h, W, p):
    """
    直接摆在距离偏好位置最近的点
    w:list of width
    h:list of height
    W:width
    p:偏好位置
    """
    n = len(w)    # 箱子总数
    ans = [[0, 0, 0, 0, 0]]      # 保存[[xi,yi,wi,hi],...]    需要排好序,以yi排序升序
    for i in range(n):
        # 开始安排第i个箱子
        tmp_h = h[i]
        tmp_w = w[i]
        tmp_p = p[i]
        tmp_intervals, tmp_y= find_position(ans,tmp_w,tmp_h,W)
        # tmp_intervals为可用的区间，下面决定三种不同的策略
        # 先考虑放在最近的点
        tmp_x = tmp_intervals[0][0]
        for j in tmp_intervals:
            if p[i] >= j[0] and p[i] <= j[1]:
                tmp_x = p[i]
                break
            elif abs(tmp_x - p[i]) > abs(j[0] - p[i]):
                tmp_x = j[0]
            elif abs(tmp_x - p[i]) > abs(j[1] - p[i]):
                tmp_x = j[1]
        tmp_ans = [tmp_x, tmp_y, tmp_w, tmp_h, tmp_p]
        for k in range(len(ans)):
            if ans[k][1] + ans[k][3] > tmp_y + tmp_h:
                ans = ans[:k] + [tmp_ans] + ans[k:]
                break
        if len(ans) != i + 2:
            ans.append(tmp_ans)
    return ans
        
def ffdtwo(w, h, W, p):
    """
    策略2
    直接摆在距离偏好位置最近的边缘点
    w:list of width
    h:list of height
    W:width
    p:偏好位置
    """
    n = len(w)    # 箱子总数
    ans = [[0, 0, 0, 0, 0]]      # 保存[[xi,yi,wi,hi],...]    需要排好序,以yi排序升序
    for i in range(n):
        # 开始安排第i个箱子
        tmp_h = h[i]
        tmp_w = w[i]
        tmp_p = p[i]
        tmp_intervals, tmp_y= find_position(ans,tmp_w,tmp_h,W)
        # tmp_intervals为可用的区间，下面决定三种不同的策略
        # 考虑放在最近的边缘点
        tmp_x = tmp_intervals[0][0]
        for j in tmp_intervals:
            # if p[i] >= j[0] and p[i] <= j[1]:
            #     tmp_x = p[i]
            #     break
            if abs(tmp_x - p[i]) > abs(j[0] - p[i]):
                tmp_x = j[0]
            elif abs(tmp_x - p[i]) > abs(j[1] - p[i]):
                tmp_x = j[1]
        tmp_ans = [tmp_x, tmp_y, tmp_w, tmp_h, tmp_p]
        for k in range(len(ans)):
            if ans[k][1] + ans[k][3] > tmp_y + tmp_h:
                ans = ans[:k] + [tmp_ans] + ans[k:]
                break
        if len(ans) != i + 2:
            ans.append(tmp_ans)
    return ans

def ffdthree(w, h, W, p):
    """
    策略3
    直接摆在距离偏好位置最近的最边缘点
    w:list of width
    h:list of height
    W:width
    p:偏好位置
    """
    n = len(w)    # 箱子总数
    ans = [[0, 0, 0, 0, 0]]      # 保存[[xi,yi,wi,hi],...]    需要排好序,以yi排序升序
    for i in range(n):
        # 开始安排第i个箱子
        tmp_h = h[i]
        tmp_w = w[i]
        tmp_p = p[i]
        tmp_intervals, tmp_y= find_position(ans,tmp_w,tmp_h,W)
        # tmp_intervals为可用的区间，下面决定三种不同的策略
        # 考虑放在最近的边缘点
        tmp_x = tmp_intervals[0][0]
        if abs(tmp_intervals[0][0] - p[i]) >= abs(tmp_intervals[-1][1] - p[i]):
            tmp_x = tmp_intervals[-1][1]
        tmp_ans = [tmp_x, tmp_y, tmp_w, tmp_h, tmp_p]
        for k in range(len(ans)):
            if ans[k][1] + ans[k][3] > tmp_y + tmp_h:
                ans = ans[:k] + [tmp_ans] + ans[k:]
                break
        if len(ans) != i + 2:
            ans.append(tmp_ans)
    return ans

def ffd_beamsearch(w, h, W, p, alpha):
    """
    带有beam_search版本的启发式算法，从三个里面选？
    w:list of width
    h:list of height
    W:width
    p:偏好位置
    """
    n = len(w)    # 箱子总数
    # beam_ans = []
    ans = [[0, 0, 0, 0, 0, 0]]      # 保存[[xi,yi,wi,hi],...]    需要排好序,以yi排序升序 第一个最后一位保存一个打分函数
    beam_ans = [ans]
    for i in range(n):
        # 开始安排第i个箱子
        tmp_h = h[i]
        tmp_w = w[i]
        tmp_p = p[i]
        tmp_beam_ans = []
        for tmp_ans in beam_ans:
            # 除了改变tmp_ans，还需要新加几个
            tmp_intervals, tmp_y= find_position(tmp_ans,tmp_w,tmp_h,W)
            # tmp_intervals为可用的区间，下面决定三种不同的策略
            # 先考虑放在最近的点
            tmp_xx = set()  #将tmp_x保存在这里面
            tmp_x = tmp_intervals[0][0]
            for j in tmp_intervals:
                if p[i] >= j[0] and p[i] <= j[1]:
                    tmp_x = p[i]
                    break
                elif abs(tmp_x - p[i]) > abs(j[0] - p[i]):
                    tmp_x = j[0]
                elif abs(tmp_x - p[i]) > abs(j[1] - p[i]):
                    tmp_x = j[1]
            tmp_xx.add(tmp_x)
            # 第二种
            tmp_x = tmp_intervals[0][0]
            for j in tmp_intervals:
            # if p[i] >= j[0] and p[i] <= j[1]:
            #     tmp_x = p[i]
            #     break
                if abs(tmp_x - p[i]) > abs(j[0] - p[i]):
                    tmp_x = j[0]
                elif abs(tmp_x - p[i]) > abs(j[1] - p[i]):
                    tmp_x = j[1]
            tmp_xx.add(tmp_x)
            # 第三种
            tmp_x = tmp_intervals[0][0]
            if abs(tmp_intervals[0][0] - p[i]) >= abs(tmp_intervals[-1][1] - p[i]):
                tmp_x = tmp_intervals[-1][1]
            tmp_xx.add(tmp_x)
            # 此时tmp_xx中保存的是可能的x坐标
            for tmp_x in tmp_xx:
                # 对三种分别进行添加
                ttmp_ans = [tmp_x, tmp_y, tmp_w, tmp_h, tmp_p]
                tmpppp_ans = copy.deepcopy(tmp_ans)
                for k in range(len(tmpppp_ans)):
                    if tmpppp_ans[k][1] + tmpppp_ans[k][3] > tmp_y + tmp_h:
                        tmpppp_ans = tmpppp_ans[:k] + [ttmp_ans] + tmpppp_ans[k:]
                        break
                if len(tmpppp_ans) != i + 2:
                    tmpppp_ans.append(ttmp_ans)
                tmpppp_ans[0][5] += abs(tmp_x - tmp_p)
                tmp_beam_ans.append(tmpppp_ans)
        # tmp_beam_ans中取出前k个s
        tmp_beam_ans.sort(key = lambda x : alpha * x[0][-1] + x[-1][1] + x[-1][3])
        beam_ans = tmp_beam_ans[:10]
    return beam_ans[0]

def find_position(p, w, h, W):
    '''
    从已经存放好的箱子中找出可存放的位置
    p: 之前已经存好的位置信息.list of [x,y,w,h]
    w: 该箱子的width
    h: 该箱子的height
    输出区间的集合[[a,b],[c,d]]
    '''
    # 先找出在y[i],y[i] + h 中有重合的箱子
    for i in range(len(p)):
        y_start = p[i][1] + p[i][3]
        y_end = y_start + h
        # 在区间[y_start, y_end]中找有重合的箱子
        tmp_intervals = []
        for j in range(len(p)):
            if p[j][1] >= y_end or p[j][1] + p[j][3] <= y_start:
                continue
            else:
                # 有交集
                tmp_intervals.append([p[j][0],p[j][0] + p[j][2]])
        # 合并区间tmp_intervals
        if tmp_intervals == []:
            return ([[0, W - w]],y_start)
        final_intervals = merge(tmp_intervals)
        # [[],[]]
        intervals = []
        tmp = 0
        for i in final_intervals:
            if i[0] - tmp >= w:
                intervals.append([tmp, i[0] - w])
            tmp = i[1]
        if W - tmp >= w:
            intervals.append([tmp, W - w])
        if len(intervals) > 0:
            return (intervals, y_start)


def merge(intervals):
    """
    合并区间
    """
    res = []
    intervals.sort(key = lambda x : x[0])
    tmp = intervals[0]
    for i in intervals:
        if i[0] > tmp[1]:
            res.append(tmp)
            tmp = i
        else:
            tmp[1] = max(tmp[1], i[1])
    res.append(tmp)
    return res   
