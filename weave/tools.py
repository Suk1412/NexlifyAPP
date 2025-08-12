def can_cover(A, B):
    """与布防图比较，判断安全区是否可以覆盖"""
    A_sorted = sorted(A, reverse=True)
    B_sorted = sorted(B, reverse=True)
    used = [False] * len(A_sorted)
    for b in B_sorted:
        found = False
        for i, a in enumerate(A_sorted):
            if not used[i] and a >= b:
                used[i] = True
                found = True
                break
        if not found:
            return False
    return True

def is_same_segment(lst):
     """找出所有安全区"""
     segments = []
     in_segment = False
     start = None
     info = {}
     for idx, item in enumerate(lst):
          if item == 1:
               if not in_segment:
                    start = idx
                    in_segment = True
          else:
               if in_segment:
                    segments.append((start, idx - 1))
                    in_segment = False
     if in_segment:
          segments.append((start, len(lst) - 1))
     for i, (start, end) in enumerate(segments, 1):
          info[i] = end - start + 1
     return info

def temporarily_set(lst, idx, value, func):
    """在安全区两边 依次踩踏 如果爆炸就记录"""
    original = lst[idx]
    lst[idx] = value
    ind = func()  # 执行中间逻辑
    lst[idx] = original
    return list(ind.values())

def landmine(condition_lst,becheck_lst):
    """排雷 找出绝对不能点的格子"""
    non_1_indices = [
        i for i, v in enumerate(becheck_lst)
        if v != 1 and (
            (i > 0 and becheck_lst[i - 1] == 1) or 
            (i < len(becheck_lst) - 1 and becheck_lst[i + 1] == 1))]
    for idx in non_1_indices:
        B = temporarily_set(becheck_lst, idx, 1, lambda: is_same_segment(becheck_lst))  # 这里只是个例子
        if not can_cover(condition_lst,B):
            becheck_lst[idx] = -1  
            
    return becheck_lst


def matrix_flat(length, matrix):
     matrix_2d = [matrix[i:i+length] for i in range(0, len(matrix), length)]  # 分行
     matrix = [item for col in [[row[j] for row in matrix_2d] for j in range(length)] for item in col]
     return matrix

def split_by_element(lst, separator):
    result = []
    temp = []
    for item in lst:
        if item == separator:
            if temp:
                result.append(temp)
                temp = []
        else:
            temp.append(item)
    if temp:
        result.append(temp)
    return result