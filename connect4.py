# Jenner Higgins
# CS 470
# Minimax algorithm w/ alpha-beta pruning

import pdb
import numpy as np
import random
from datetime import datetime

ROWS = 6        # number of rows in connect 4
COLS = 7        # number of columns in conncect 4 
WIN_CON = 4     # win condition
PLAYER = 0      # player 1
AI = 1          # ai player

def createGrid():
    grid = np.zeros((ROWS, COLS)) # 6 rows x 7 columns
    return grid

def isValidMove(grid, move):
    if(move < 0 or move > COLS - 1):
        return False
    else:
        return grid[ROWS - 1][move] == 0

def getValidMoves(grid):
    valid_spots = []
    for c in range(COLS):
        if(isValidMove(grid, c)):
            valid_spots.append(c)
    return valid_spots

def getOpenRow(grid, move):
    for r in range(ROWS):
        if(grid[r][move] == 0):
            return r

def placeMove(grid, row, col, piece):
    grid[row][col] = piece

def printGrid(grid):
    print(np.flip(grid, 0)) # flip board across x-axis

def checkWin(grid, piece): # TODO – checkWin() could be cleaner and more efficient
    for c in range(COLS - 3):
        for r in range(ROWS):
            if(grid[r][c] == piece and grid[r][c + 1] == piece and
            grid[r][c + 2] == piece and grid[r][c + 3] == piece):
                return True

    for r in range(ROWS - 3):
        for c in range(COLS):
            if(grid[r][c] == piece and grid[r + 1][c] == piece and
            grid[r + 2][c] == piece and grid[r + 3][c] == piece):
                return True

        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if(grid[r][c] == piece and grid[r + 1][c + 1] == piece and
                grid[r + 2][c + 2] == piece and grid[r + 3][c + 3] == piece):
                    return True

    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if(grid[r][c] == piece and grid[r - 1][c + 1] == piece and
            grid[r - 2][c + 2] == piece and grid[r - 3][c + 3] == piece):
                return True

def evaluate(streak, piece):
    score = 0
    player_piece = 1

    if(streak.count(piece) == 3 and streak.count(0) == 1):
        score += 75
    elif(streak.count(piece) == 2 and streak.count(0) == 2):
        score += 20

    if(streak.count(player_piece) == 3 and streak.count(0) == 1):
        score -= 100
    elif(streak.count(player_piece) == 2 and streak.count(0) == 2):
        score -= 5

    return score


def findMove(grid, piece):
    score = 0

    middle_col_list = [int(i) for i in list(grid[:,COLS//2])]
    center_count = middle_col_list.count(piece)
    score += center_count * 20

    for c in range(COLS):
        col_list = [int(i) for i in list(grid[:,c])]
        for r in range(ROWS - 3):
            streak = col_list[r : r + WIN_CON]
            score += evaluate(streak, piece)

    for r in range(ROWS):
        row_list = [int(i) for i in list(grid[r,:])]
        for c in range(COLS - 3):
            streak = row_list[c : c + WIN_CON]
            score += evaluate(streak, piece)

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            streak = [grid[r + i][c + i] for i in range(WIN_CON)]
            score += evaluate(streak, piece)

    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            streak = [grid[r + 3 - i][c + i] for i in range(WIN_CON)]
            score += evaluate(streak, piece)

    return score

def isTerminal(grid):
    return checkWin(grid, 1) or checkWin(grid, 2) or len(getValidMoves(grid)) == 0

def minimax(grid, depth, alpha, beta, isMax):
    legal_moves = getValidMoves(grid)
    is_terminal = isTerminal(grid)
    if(depth == 0 or is_terminal):
        if(is_terminal):
            #breakpoint()
            if(checkWin(grid, 2)): # AI
                return (None, 100000000)
            elif(checkWin(grid, 1)): # Player
                return (None, -100000000)
            else: # tie
                return (None, 0)
        else:
            return (None, findMove(grid, 2))

    if(isMax):
        value = -1000000
        move = 3
        for c in legal_moves:
            row = getOpenRow(grid, c)
            temp_grid = grid.copy()
            placeMove(temp_grid, row, c, 2)
            score = minimax(temp_grid, depth - 1, alpha, beta, False)[1]
            if score > value:
                value = score
                move = c
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (move, value)
    else:
        value = 1000000
        move = 3
        for c in legal_moves:
            row = getOpenRow(grid, c)
            temp_grid = grid.copy()
            placeMove(temp_grid, row, c, 1)
            score = minimax(temp_grid, depth - 1, alpha, beta, True)[1]
            if score < value:
                value = score
                move = c
            alpha = min(alpha, value)
            if alpha >= beta:
                break
        return (move, value)

grid = createGrid()
game_over = False

choice = int(input("Enter [1, 2] to choose play order: "))
if(choice == 1):
    turn = 0
elif(choice == 2):
    turn = 1
else:
    print("Invalid choice. Restart program to try again.")
    exit(0)

printGrid(grid)

while not game_over:
    if turn == PLAYER: # Player
        try:
            move = int(input("Player turn, enter number between [0, 6]: "))
            if(isValidMove(grid, move)):
                row = getOpenRow(grid, move)
                placeMove(grid, row, move, 1)
                printGrid(grid)
                turn += 1
                turn = turn % 2
                if(checkWin(grid, 1)):
                    print("Player wins!")
                    game_over = True
                elif(len(getValidMoves(grid)) == 0):
                    print("It's a tie")
                    game_over = True
            else:
                print("Invalid move. Please try again.") # QUESTION: redundant error case?
                continue # QUESTION: bad practice/avoidable?
        except:
            print("Invalid input. Please try again.")

    if turn == AI and not game_over: # AI
        try:
            print("AI turn...")
            time = datetime.now()
            move, minimax_value = minimax(grid, 5, -1000000, 1000000, True)
            time = datetime.now() - time
            if(isValidMove(grid, move)):
                row = getOpenRow(grid, move)
                placeMove(grid, row, move, 2)
                print("AI chose location: ({},{}) in {}s".format(row, move, time))
                printGrid(grid)
                turn += 1
                turn = turn % 2
                if(checkWin(grid, 2)):
                    print("AI wins!")
                    game_over = True
                elif(len(getValidMoves(grid)) == 0):
                    print("It's a tie")
                    game_over = True
            else:
                print("Invalid location. Please try again.")
        except:
            print("AI ERROR")
            exit(-1)
