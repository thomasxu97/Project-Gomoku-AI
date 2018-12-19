from Gomoku_ver_3 import *
import numpy as np

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
'''
B = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,2,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]


ai.boardScore.boardScoreInitialization(B, 1)
ai.board = B
ai.boardScore.debugPrintAll()
ai.ban = ME
AIFirst = True
ai.hand = 1
'''
p = False
while True:
    '''
    if (AIFirst):
        place = ai.turn()
        ai.board[place[0]][place[1]] = ME
        print("-----------------------------------------------")
        AIFirst = False
    '''

    debugprintboard(ai.board)
    row = input("Please input #row:")
    if row == "print":
        #ai.boardScore.debugPrintAll()
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
    place = ai.turn()
    print(place)
    ai.board[place[0]][place[1]] = ME
    print("-----------------------------------------------")


