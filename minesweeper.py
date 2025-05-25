'''
Game rule 💣:

The goal of Minesweeper is to reveal all safe tiles without uncovering any mines. 

Each tile may contain a number (1-8) indicating how many mines are adjacent, a mine (💣),
or nothing (an empty tile, which will trigger a flood reveal of neighboring empty tiles). 

You can reveal a tile using 'r row col', flag/unflag a tile with 'f row col', and quit the game with 'q'. 

Flagged tiles cannot be revealed unless unflagged first. 

The game ends when all safe tiles are revealed (you win) or when a mine is revealed (you lose).

Use logic and the numbers to identify where the hidden mines are.

'''


import random

# Choose the size of game
def choose_difficulty():
    print("Choose your difficulty level: ")
    print("1. primary(9x9, 10 mines)")
    print("2. middle(16x16, 40 mines)")
    print("3. advanced(30x16, 99 mines)")
    
    choice = input("Your difficulty level(1/2/3): ").strip()
    if choice == '1':
        return 9, 9, 10
    elif choice == '2':
        return 16, 16, 40
    elif choice == '3':
        return 16, 30, 99
    else:
        print("Invalid input.")
        return 9, 9, 10

# Create the initial board
def init_board(rows, cols, num_mines):
    board = [[{'is_mine': False,  # whether a mine
               'is_revealed': False, # whether be revealed
               'is_flagged': False, # whether be flagged
               'adjacent': 0 # how many mines around the cell (default 0)
               }for _ in range(cols)] for _ in range(rows)]
    
    # Place mines randomly
    mines = random.sample(range(rows * cols), num_mines) # place mines
    #print(mines)
    for idx in mines:
        r = idx // cols # row
        c = idx % cols # cols
        board[r][c]['is_mine'] = True

    # caculate mines num
    for r in range(rows):
        for c in range(cols):
            if board[r][c]['is_mine']:
                continue
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc]['is_mine']:
                        count += 1
            board[r][c]['adjacent'] = count
    return board

# reveal the cell
def reveal(board, r, c, rows, cols):
    if not (0 <= r < rows and 0 <= c < cols): # check whether out of range
        return
    cell = board[r][c]
    if cell['is_revealed'] or cell['is_flagged']:
        return
    cell['is_revealed'] = True
    if cell['adjacent'] == 0 and not cell['is_mine']:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr != 0 or dc != 0:
                    reveal(board, r + dr, c + dc, rows, cols)

# count flags num
def count_flags(board):
    count = 0
    for row in board:
        for cell in row:
            if cell['is_flagged']:
                count += 1
    return count

# print board
def print_board(board, rows, cols, num_mines):
    flags = count_flags(board)
    print(f"\nNumber of mines remaining (estimated): {num_mines - flags}")
    print("    ", end="")
    for c in range(cols):
        print(f"{c:2}", end=" ")
    print()
    print("   " + "---" * cols)

    for r in range(rows):
        print(f"{r:2} |", end=" ")
        for c in range(cols):
            cell = board[r][c]
            if cell['is_flagged']:
                ch = '⚑'
            elif not cell['is_revealed']:
                ch = '□'
            elif cell['is_mine']:
                ch = '*' # mine
            elif cell['adjacent'] > 0:
                ch = str(cell['adjacent'])
            else:
                ch = ' '
            print(f"{ch:^2}", end=" ")
        print()

# check victory
def check_win(board, rows, cols):
    for r in range(rows):
        for c in range(cols):
            cell = board[r][c]
            if not cell['is_mine'] and not cell['is_revealed']:
                return False
    return True

# main play
def play():
    rows, cols, num_mines = choose_difficulty()
    board = init_board(rows, cols, num_mines)

    while True:
        print_board(board, rows, cols, num_mines)
        cmd_raw = input("Enter your operation (e.g. 'r 2 3' to reveal, 'f 1 4' to flag, or 'q' to quit): ")
        if cmd_raw.lower() == 'q':
            print("👋 Game closed. Thanks for playing!")
            return
            #exit(0)

        cmd = cmd_raw.split()

        if len(cmd) != 3:
            print("Wrong format, please input: r 3 4 or f 2 1")
            continue
        op, r, c = cmd[0], int(cmd[1]), int(cmd[2])
        if not (0 <= r < rows and 0 <= c < cols):
            print("Invalid coordinates.")
            continue
        cell = board[r][c]

        if op == 'f':
            cell['is_flagged'] = not cell['is_flagged']
            if cell['is_flagged']:
                print("🚩 Tile flagged.")
            else:
                print("❌ Flag removed.")
        elif op == 'r':
            if cell['is_flagged']:
                print("Cannot reveal a flagged cell.")
                continue
            if cell['is_mine']:
                cell['is_revealed'] = True
                print_board(board, rows, cols, num_mines)
                print("💥 Boom! You hit a mine. Game over!")
                return
            reveal(board, r, c, rows, cols)
            if check_win(board, rows, cols):
                print_board(board, rows, cols, num_mines)
                print("🎉 Congratulations! You win!")
                return
        else:
            print("Invalid command. Please use 'r' to reveal or 'f' to flag or 'q' to quit the game.")



if __name__ == "__main__":
    play()
