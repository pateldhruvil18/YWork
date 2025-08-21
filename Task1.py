def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == ".":  
                return (i, j)
    return None

def valid(board, num, pos):
    row, col = pos

    for j in range(9):
        if board[row][j] == str(num) and col != j:
            return False

    for i in range(9):
        if board[i][col] == str(num) and row != i:
            return False

    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == str(num) and (i, j) != pos:
                return False

    return True

def solve(board):
    find = find_empty(board)
    if not find:
        return True  
    row, col = find

    for num in range(1, 10):
        if valid(board, num, (row, col)):
            board[row][col] = str(num)
            if solve(board):
                return True
            board[row][col] = "."
    return False



# main:->

board = []

print("Enter your Sudoku puzzle (9 rows, use '.' for empty cells):")
for i in range(9):
    row = input(f"Row {i+1}: ").split()
    if len(row) != 9:
        raise ValueError("Each row must have exactly 9 values (digits or .)")
    board.append(row)

print("\nInitial Board:")
print_board(board)

if solve(board):
    print("\nSolved Board:")
    print_board(board)
else:
    print("No solution exists for this puzzle!")
