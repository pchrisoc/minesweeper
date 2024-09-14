import random

class Board:

    def __init__(self, board_size, num_bombs):
        self.board_size = board_size
        self.num_bombs = num_bombs

        self.board = self.make_new_board()  # Plants bombs
        self.assign_value_to_board()

        self.dug = set()  # Saves in coordinates: (row,col)

    def make_new_board(self):
        # Makes a new board with mines
        board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        #creates a grid 
        #plants bombs
        planted_bombs = 0
        while planted_bombs < self.num_bombs:
            loc = random.randint(0, self.board_size**2 - 1)
            row = loc // self.board_size #tells the code which row to look at 
            col = loc % self.board_size #tells the code to look at a certain index by getting the remainder

            if board[row][col] == '*': 
                continue
            board[row][col] = '*' # plants the bomb
            planted_bombs += 1

        return board

    def assign_value_to_board(self): #assigns values to empty spaces in grid
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.grab_num_neighbor_bombs(r, c)
         
    def grab_num_neighbor_bombs(self, row, col): #iterates through neighboring positions of coordinates and bombs
        
        """
        Count the number of neighboring bombs around the specified coordinates.

        Example:
        >>> board = Board(3, 1)
        >>> board.make_new_board() #doctest:+ELLIPSIS
        [...]
        >>> 0 <= board.grab_num_neighbor_bombs(0, 0) <= 3 #Count neighboring bombs for an empty cell
        True
        >>> 0 <= board.grab_num_neighbor_bombs(1, 1) <= 8 #Count neighboring bombs for a cell with a bomb
        True
        >>> 0 <= board.grab_num_neighbor_bombs(2, 2) <= 5 #Count neighboring bombs for a cell surrounded by bombs
        True
        >>> 0 <= board.grab_num_neighbor_bombs(0, 2) <= 3 #Count neighboring bombs for a cell in the corner
        True
        >>> 0 <= board.grab_num_neighbor_bombs(1, 0) <= 5 #Count neighboring bombs for a cell on the edge
        True
        """
        
        num_neighbor_bombs = 0
        for r in range(max(0, row-1), min(self.board_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.board_size-1, col+1)+1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_neighbor_bombs += 1
        return num_neighbor_bombs

    def dig(self, row, col): 
        # Location where it digs
        # True if successful, False if bomb is struck
        self.dug.add((row, col))
        if self.board[row][col] == "*":
            return False
        if self.board[row][col] > 0:
            return True
        
        for r in range(max(0,row-1), min(self.board_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.board_size-1, col+1)+1):
                if (r,c) in self.dug:
                    continue
                self.dig(r,c)
        return True

    def __str__(self): #shows the output as a string, displaying the grid in the terminal
        # creates a grid that the user sees, physical representation of the array
        visible_board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        string_rep = ''
        widths = []
        for idx in range(self.board_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key=len)))
        # prints CSV strings
        indices = [i for i in range(self.board_size)]
        indices_row = '      '
        cells = []
        for idx, col in enumerate(indices):
            format_str = '%-' + str(widths[idx]) + "s"
            cells.append(format_str % (col))
        indices_row += '   '.join(cells)
        indices_row += '\n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'  {i} | '
            cells = []
            for idx, col in enumerate(row):
                format_str = '%-' + str(widths[idx]) + "s"
                cells.append(format_str % (col))
            string_rep += ' | '.join(cells)
            string_rep += ' | \n'
        str_len = int(len(string_rep) / self.board_size)
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep


def play(board_size=10, num_bombs=10):
    board = Board(board_size, num_bombs)  # Creates board and places bombs
    safe = True
    while len(board.dug) < board_size ** 2 - num_bombs:
        print(board)
        user_input = input("Dig Placement (row,col): ").split(',')
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.board_size or col < 0 or col >= board.board_size:  # Checks if coordinates are in correct bounds
            print("Invalid Coordinate")
            continue

        # If placement is valid, we dig
        safe = board.dig(row, col)
        if not safe:
            break  # game over

    if safe:
        print("Victory Royale!")
    else:
        print("Give up, you suck.")
        # Reveal board:
        board.dug = {(r, c) for r in range(board.board_size) for c in range(board.board_size)}
        print(board)

if __name__ == "__main__": #Game starts by refering to file in terminal "python3 minesweeper.py"
    play()