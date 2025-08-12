import itertools
import copy

def get_1_blocks(lst):
    """获取列表中连续的1块长度列表"""
    return [len(list(g)) for k, g in itertools.groupby(lst) if k == 1]

def matches_B(lst, condition_lst):
    """判断列表是否包含 condition_lst 中所需的所有连续1块"""
    block_list = get_1_blocks(lst)
    temp = block_list.copy()
    for b in condition_lst:
        if b in temp:
            temp.remove(b)
        else:
            return False
    return True

def map_list(a):
    """将列表映射为只包含1和-1：1保留，其它视为-1"""
    return [1 if x == 1 else -1 for x in a]

def check_critical_positions(condition_lst,becheck_lst):
    # 找出所有非1非-1元素的索引（可变项）
    print("条件列表：",condition_lst)
    print("检查：",becheck_lst)
    result = True
    modifiable_indices = [i for i, val in enumerate(becheck_lst) if val != 1 and val != -1]
    correct_list = []
    # 遍历每一个可变位置
    for idx in modifiable_indices:
        A_copy = becheck_lst.copy()
        original_value = A_copy[idx]

        # 将当前这个改为 -1
        A_copy[idx] = -1

        # 其他所有非1非-1的位置，改为 1
        for j in modifiable_indices:
            if j != idx:
                A_copy[j] = 1

        # 转换后判断是否仍满足 condition_lst
        mapped = map_list(A_copy)
        result = matches_B(mapped, condition_lst)
        print(f"将索引 {idx} 的元素 {original_value} 改为 -1，"
            f"其余可变项设为 1 后是否仍满足 condition_lst: {result}")
        if not result:
            correct_list.append(original_value)
    return correct_list
    


if __name__ == '__main__':
    # 原始数据
    becheck_lst = [(2, 1) ,1 ,1 ,-1 ,1 ,-1 ,-1 ,(2, 8) ,(2, 9) ,(2, 10)]
    condition_lst = [3, 1, 1]
    if not check_critical_positions(condition_lst,becheck_lst):
        print("改成1")
    else:
        print("不用改")