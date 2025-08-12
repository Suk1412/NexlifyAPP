from itertools import product, groupby
from collections import Counter

def get_1_blocks(lst):
    return [len(list(g)) for k, g in groupby(lst) if k == 1]

def matches_B(lst, condition_lst):
    block_list = get_1_blocks(lst)
    count_blocks = Counter(block_list)
    count_condition = Counter(condition_lst)
    for k in count_condition:
        if count_blocks[k] < count_condition[k]:
            return False
    return True

def can_satisfy_condition_by_any_combination(condition_lst, becheck_lst):
    modifiable_indices = [i for i, val in enumerate(becheck_lst) if val != 1 and val != -1]

    # 枚举所有 2^n 的可能组合
    for comb in product([1, -1], repeat=len(modifiable_indices)):
        A_copy = becheck_lst.copy()
        for idx, val in zip(modifiable_indices, comb):
            A_copy[idx] = val

        mapped = [1 if x == 1 else -1 for x in A_copy]
        if matches_B(mapped, condition_lst):
            print(f"找到满足条件的组合：{comb}")
            return True
    return False
if __name__ == '__main__': 
    
    becheck_lst = [(2, 1) ,1 ,1 ,-1 ,1 ,-1 ,-1 ,(2, 8) ,(2, 9) ,(2, 10)]
    condition_lst = [3, 1, 1]     
    print()


"d41220",
"d513",
"d43202000b0a",
"d533",
"d4320400",
"d533",
"d43205010001",
"d533",
"d4320a59f43f114d85616f266287",
"d533",
"d4320b69ff3f114185616f",
"d533",
"d4320cff0485",
"d533",
"d4320d85158a8508b28501da",
"d533",
"d4086316ff",
"d509",
"d4320102",
"d533",