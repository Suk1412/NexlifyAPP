from copy import deepcopy

UNKNOWN = -1
EMPTY = 0
FILLED = 1

def line_fits(line, clues):
    """
    判断给定行（或列）状态是否能满足 clues 约束
    line: [FILLED, EMPTY, UNKNOWN...] 状态列表
    clues: [数字, 数字,...] 规则提示
    """
    groups = []
    count = 0

    for cell in line:
        if cell == FILLED:
            count += 1
        else:
            if count > 0:
                groups.append(count)
                count = 0
    if count > 0:
        groups.append(count)

    # 早期剪枝：检查已有组数是否超过 clues，或已超长
    if len(groups) > len(clues):
        return False

    # 逐组比较，部分确定时只要符合前缀即可
    for g, c in zip(groups, clues):
        if g > c:
            return False

    # 如果行里没有 UNKNOWN，组数必须完全匹配
    if UNKNOWN not in line and groups != clues:
        return False

    # 合理，否则可能是正确或者不确定
    return True

def generate_line_possibilities(length, clues):
    """
    生成所有满足 clues 约束的长度为 length 的序列
    (用于辅助构造解空间，可选)
    """
    # 递归构造函数
    def backtrack(clues_idx, pos, current):
        if clues_idx == len(clues):
            if len(current) == length:
                yield current
            else:
                # 剩余全空
                yield current + [EMPTY]*(length - len(current))
            return

        clue = clues[clues_idx]
        max_start = length - sum(clues[clues_idx:]) - (len(clues) - clues_idx -1)
        for start in range(pos, max_start+1):
            new_line = current + [EMPTY]*(start - len(current)) + [FILLED]*clue
            if clues_idx < len(clues) - 1:
                new_line.append(EMPTY)
            yield from backtrack(clues_idx+1, len(new_line), new_line)

    return backtrack(0,0,[])

def transpose(board):
    return [list(row) for row in zip(*board)]

def is_solved(board):
    for row in board:
        if UNKNOWN in row:
            return False
    return True

def check_board(board, row_clues, col_clues):
    for r, clues in enumerate(row_clues):
        if not line_fits(board[r], clues):
            return False
    for c, clues in enumerate(col_clues):
        col = [board[r][c] for r in range(len(board))]
        if not line_fits(col, clues):
            return False
    return True

def solve_nonogram(board, row_clues, col_clues):
    """
    递归回溯求解非ogram
    board: 当前棋盘状态，二维列表
    row_clues, col_clues: 提示数字列表
    返回：解的board，失败返回 None
    """
    if is_solved(board):
        if check_board(board, row_clues, col_clues):
            return board
        else:
            return None

    # 选一个未知格子，优先挑最约束的
    height = len(board)
    width = len(board[0])

    # 简单启发：按未知数量最少的行或列处理
    # 这里简单选第一个未知格子
    for r in range(height):
        for c in range(width):
            if board[r][c] == UNKNOWN:
                # 尝试填 FILLED
                new_board = deepcopy(board)
                new_board[r][c] = FILLED
                if check_board(new_board, row_clues, col_clues):
                    result = solve_nonogram(new_board, row_clues, col_clues)
                    if result:
                        return result
                # 尝试填 EMPTY
                new_board[r][c] = EMPTY
                if check_board(new_board, row_clues, col_clues):
                    result = solve_nonogram(new_board, row_clues, col_clues)
                    if result:
                        return result
                # 两个尝试都失败，回溯
                return None
    return None

def print_board(board):
    symbols = {UNKNOWN: '○', EMPTY: '□', FILLED: '■'}
    for row in board:
        print(' '.join(symbols[cell] for cell in row))

if __name__ == "__main__":
    row_clues = [
    [8],
    [3,1,1],
    [5,2,1],
    [3,1,2,1],
    [3,1],
    [1,1,1,1],
    [3,1,1,1],
    [5,1,1],
    [3,1,1],
    [8],
    ]
    col_clues = [
    [3,3],
    [4,4],
    [10],
    [1,1,1,1,1],
    [10],
    [1,1],
    [1,2,1,1,1],
    [1,2,1,1],
    [2,2],
    [6]
    ]

    # 初始化棋盘
    height = len(row_clues)
    width = len(col_clues)
    board_default = [[UNKNOWN]*width for _ in range(height)]   
    solution = solve_nonogram(board_default, row_clues, col_clues)
    print(solution)
    if solution:
        print("找到解:")
        print_board(solution)
    else:
        print("无解")
