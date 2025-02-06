from SudokuBoard import SudokuBoard
import sys
import pprint
import time
import argparse

def set_domains(sudoku_puzzle):
    n = 9
    domains = [[[1, 2, 3, 4, 5, 6, 7, 8,9] for j in range(n)] for i in range(n)]
    
    for i in range(len(sudoku_puzzle.board)):
        for j in range(len(sudoku_puzzle.board[i])):
            val = sudoku_puzzle.board[i][j]
            if (val != 0):
                domains[i][j] = [-1]
                constrict_domains(sudoku_puzzle, i, j, val, domains)
                if(len(domains[i][j]) == 0):
                    print("IMPOSSIBLE TABLE: There are no possible values for", 
                    [i,j])
                    exit(0)
    return domains  



def constrict_domains(sudoku_puzzle, row, col, num, domains):

    constrict_box_domains(sudoku_puzzle, row, col, num, domains)

    constrict_row_domains(sudoku_puzzle, row, col, num, domains)


    constrict_col_domains(sudoku_puzzle, row, col, num, domains)



def constrict_box_domains(sudoku_puzzle, row, col, num, domains):
    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if (num in domains[i][j] and [i,j] != [row, col]
                and sudoku_puzzle.board[i][j] == 0):
                domains[i][j].remove(num)



def constrict_row_domains(sudoku_puzzle, row, col, num, domains):
    for j in range(len(sudoku_puzzle.board[row])):
        if (num in domains[row][j] and col != j
            and sudoku_puzzle.board[row][j] == 0):
            domains[row][j].remove(num)


def constrict_col_domains(sudoku_puzzle, row, col, num, domains):
    for i in range(len(sudoku_puzzle.board)):
        if (num in domains[i][col] and row != i
            and sudoku_puzzle.board[i][col] == 0):
            domains[i][col].remove(num)



def empty_domain(sudoku_puzzle, domains):
    for i in range(len(sudoku_puzzle.board)):
        for j in range(len(sudoku_puzzle.board[i])):
            if(sudoku_puzzle.board[i][j] == 0 and len(domains[i][j]) == 0):
                return [i, j]
    
    return False


def find_empty_domain(sudoku_puzzle, domains):
    for i in range(len(domains)):
        for j in range(len(domains[i])):
            if(len(domains[i][j]) == 0 and sudoku_puzzle.board[i][j] == 0):
                return [i, j]



def repair_domains(sudoku_puzzle, row, col, num, domains):

    repair_box_domains(sudoku_puzzle, row, col, num, domains)


    repair_row_domains(sudoku_puzzle, row, col, num, domains)


    repair_col_domains(sudoku_puzzle, row, col, num, domains)


def repair_box_domains(sudoku_puzzle, row, col, num, domains):
    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if (num not in domains[i][j] and [i,j] != [row, col] 
            and sudoku_puzzle.valid_input(i,j,num)):
                domains[i][j].append(num)


def repair_row_domains(sudoku_puzzle, row, col, num, domains):
    for j in range(len(sudoku_puzzle.board[row])):
        if (num not in domains[row][j] and col != j 
        and sudoku_puzzle.valid_input(row, j, num)):
            domains[row][j].append(num)



def repair_col_domains(sudoku_puzzle, row, col, num, domains):
    for i in range(len(sudoku_puzzle.board)):
        if (num not in domains[i][col] and row != i 
        and sudoku_puzzle.valid_input(i, col, num)):
            domains[i][col].append(num)




def find_empty_basic(sudoku_puzzle, domains):
    for i in range(len(sudoku_puzzle.board)):
        for j in range(len(sudoku_puzzle.board[i])):
            if (sudoku_puzzle.board[i][j] == 0):
                return [i, j]
    return False



def backtracking(sudoku_puzzle, heuristic):
    domains = set_domains(sudoku_puzzle)

    backtracking_rec(sudoku_puzzle, heuristic, domains)


def backtracking_rec(sudoku_puzzle, heuristic, domains):
    next = heuristic(sudoku_puzzle, domains)
    if not next:
        return True
    else:
        sudoku_puzzle.unique_states += 1 

        row = next[0]
        col = next[1]

    for i in range(1,10):
        if sudoku_puzzle.valid_input(row, col, i):
            sudoku_puzzle.board[row][col] = i

            if backtracking_rec(sudoku_puzzle, heuristic, domains):
                return True

        sudoku_puzzle.board[row][col] = 0

    return False




def forward_checking(sudoku_puzzle, heuristic):
    domains = set_domains(sudoku_puzzle)

    forward_checking_rec(sudoku_puzzle, heuristic, domains)


def forward_checking_rec(sudoku_puzzle, heuristic, domains):
    next = heuristic(sudoku_puzzle, domains)
    if (not next):
        return True
    else:
        sudoku_puzzle.unique_states += 1 

        row = next[0]
        col = next[1]
 
    for x in domains[row][col]:
        sudoku_puzzle.board[row][col] = x
        constrict_domains(sudoku_puzzle, row, col, x, domains)

        if (not empty_domain(sudoku_puzzle, domains)):
        
            if forward_checking_rec(sudoku_puzzle, heuristic, domains):
                return True

            
        sudoku_puzzle.board[row][col] = 0
        repair_domains(sudoku_puzzle, row, col, x, domains)
        
    return False





def update_conflictsets(sudoku_puzzle, row, col, num, domains):
    update_box_conflictsets(sudoku_puzzle, row, col, num, domains)
    constrict_box_domains(sudoku_puzzle, row, col, num, domains)

    update_row_conflictsets(sudoku_puzzle, row, col, num, domains) 
    constrict_row_domains(sudoku_puzzle, row, col, num, domains)

    update_col_conflictsets(sudoku_puzzle, row, col, num, domains)
    constrict_col_domains(sudoku_puzzle, row, col, num, domains)


def update_box_conflictsets(sudoku_puzzle, row, col, num, domains):
    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if (num in domains[i][j] and [i,j] != [row, col] 
                and sudoku_puzzle.board[i][j] == 0):
                sudoku_puzzle.conflict_stacks[i][j].append([row, col])
                


def update_row_conflictsets(sudoku_puzzle, row, col, num, domains):
    for j in range(len(sudoku_puzzle.board[row])):
        if (num in domains[row][j] and col != j
            and sudoku_puzzle.board[row][j] == 0):
            sudoku_puzzle.conflict_stacks[row][j].append([row, col])



def update_col_conflictsets(sudoku_puzzle, row, col, num, domains):
    for i in range(len(sudoku_puzzle.board)):
        if (num in domains[i][col] and row != i 
            and sudoku_puzzle.board[i][col] == 0):
            sudoku_puzzle.conflict_stacks[i][col].append([row, col])


def repair_conflictset(sudoku_puzzle, row, col):
    # [row, col] should be removed from all conflict stacks since it is no longer assigned

    for i in range(len(sudoku_puzzle.board)):
        for j in range(len(sudoku_puzzle.board[i])):
            if ([row,col] in sudoku_puzzle.conflict_stacks[i][j]):
                sudoku_puzzle.conflict_stacks[i][j].remove([row, col])


# main function
if __name__ == '__main__':
    start_time = time.time()
    
    board_name = parse_arguments()

    with open(board_name, 'r') as boards_file:
        game = SudokuBoard(boards_file)
        
        forward_checking(game, find_empty_basic)

        print("Unique States: ", game.unique_states)

        game.print_board()

        print("--- %s seconds ---" % round((time.time() - start_time), 3)) 
