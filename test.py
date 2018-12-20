from Gomoku_ver_4 import *
import numpy as np
import time

def debugprintboard(board):
    print("    ", end = '')
    for i in range(BOARD_SIZE):
        print("%-3d"%(i), end = '')
    print("")
    for i in range(BOARD_SIZE):
        print("%-3d"%(i), end = '')
        for j in range(BOARD_SIZE):
            if (board[i][j] == ME):
                print(" * ", end = '')
            elif (board[i][j] == OTHER):
                print(" # ", end = '')
            else:
                print("   ", end = '')
        print("")

ai = AI()

B = np.zeros((BOARD_SIZE, BOARD_SIZE))
B[7][7] = OTHER
B[7][6] = ME
B[8][9] = OTHER

ai.boardScore.boardScoreInitialization(B, OTHER)
ai.board = B
# ai.boardScore.debugPrintAll()
ai.ban = OTHER
AIFirst = True
ai.hand = 1

p = False
while True:

    if (AIFirst):
        place = ai.turn()
        ai.board[place[0]][place[1]] = ME
        print("-----------------------------------------------")
        AIFirst = False


    debugprintboard(ai.board)
    row = input("Please input #row:")
    if row == "print":
        ai.boardScore.debugPrintAll()
        p = True
        debugprintboard(ai.board)
        row = input("Please input #row:")
    row = int(row)
    col = int(input("Please input #col:"))
    

    ai.board[row][col] = OTHER
    ai.boardScore.boardScoreUpdate(OTHER, [row, col])
    if p:
        ai.boardScore.debugPrintAll()
        p = False
    debugprintboard(ai.board)
    t0 = time.time()
    place = ai.turn()
    t1 = time.time()
    print(place)
    print("Taking time: " + str((t1-t0) * 1000))
    ai.board[place[0]][place[1]] = ME
    print("-----------------------------------------------")


