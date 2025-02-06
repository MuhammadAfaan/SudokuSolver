from SudokuError import SudokuError
from copy import copy, deepcopy

class SudokuBoard(object):
    
    def __init__(self, input_file):
        self.__initialize_board(input_file)
        self.unique_states      = 1
        self.conflict_stacks    = [[[] for j in range(9)] for i in range(9)]
        self.backjump           = [-1, -1]
        self.gameover           = False

    
    def start_over(self):
        self.board = deepcopy(self.start_board)

    def print_board(self):
        for i in range(len(self.board)):
            if (i % 3 == 0 and i != 0):
                print("------+-------+-------")

            for j in range(len(self.board[i])):
                if (j % 3 == 0 and j != 0):
                    print("|", end = " ")

                print(self.board[i][j], end = " ")
            print()


    def valid_input(self, row, col, num):
        return (self.__valid_box(row, col, num) 
                and self.__valid_row(row, col, num) 
                and self.__valid_col(row, col, num))

    
    def combine_conflicts(self, source, dest):
        for to_add in reversed(source):
            if(to_add not in dest):
                # print("Adding", to_add, "to", dest)
                dest.insert(0, to_add)


    def check_win(self):
        for i in range(len((self.board))):
            for j in range(len(self.board[i])):
                if not self.valid_input(i, j, self.board[i][j]):
                    return False
        self.gameover = True
        return True


    def __initialize_board(self, input):
        input_lines = input.readlines()

        self.board = [[0 for j in range(9)] for i in range(9)]

        for i in range(len(input_lines)):
            if(len(input_lines[i]) != 18):
                raise SudokuError(
                    "Each line in the sudoku puzzle must be 18 chars long."
                )
            
            for j in range(0, 18, 2):
                if (not input_lines[i][j].isdigit()):
                    raise SudokuError(
                        "Valid characters for a sudoku puzzle must be in 0-9"
                    )
                
                self.board[i][j // 2] = int(input_lines[i][j])

        input.close()

        if(not self.__valid_table()):
            raise SudokuError(
                "IMPOSSIBLE TABLE: Conflicts already exists"
            )
        
        self.start_board = deepcopy(self.board)


    def __valid_table(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (self.board[i][j] != 0 
                    and not self.valid_input(i, j, self.board[i][j])):
                    print([i, j])
                    return False
        return True

    def __valid_box(self, row, col, num):
        box_x = col // 3
        box_y = row // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if (self.board[i][j] == num and i != row and j != col):
                    # print("Not Valid B")
                    return False
        return True

    def __valid_row(self, row, col, num):
        for j in range(len(self.board[row])):
            if (self.board[row][j] == num and col != j):
                # print("Not Valid r")
                return False
        return True

    
    def __valid_col(self, row, col, num):
        for i in range(len(self.board)):
            if (self.board[i][col] == num and row != i):
                # print("Not Valid C")
                return False
        return True