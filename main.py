# -*- coding: utf-8 -*-

START = "START"
PLACE = "PLACE"
DONE = "DONE"
TURN = "TURN"
BEGIN = "BEGIN"
END = "END"

BOARD_SIZE = 15
EMPTY = 0
ME = 1
OTHER = 2

def getlinescore(line):
    # return the score of a line (my score - opponent score)
        #five = 10000
        #four = 1000
        #three = 100
        #two = 10
        #one =1

        #dead four = 100
        #dead three = 10
        #dead two = 1
    # currently 1 1 0 1 not considered as three (bad) 1 1 0 1 1 not considered as four (bad)
    # currently 禁手 not condidered (bad)
    dead = 1
    count = 0
    score = 0
    me = False
    for i in range(len(line)):
        if line[i] == EMPTY:
            if count != 0:
                if me:
                    if count > 4:
                        score = 10000
                        return score
                    score += int(10**(count-dead-1))
                    count = 0
                else:
                    if count > 4:
                        score = -10000
                        return score
                    score -= int(10**(count-dead-1))
                    count = 0
            dead = 0
        elif line[i] == ME:
            if count == 0 or me:
                count += 1
            else:
                if count > 4:
                    score = -10000
                    return score
                if dead != 1:
                    score -= int(10**(count-2))
                count = 1
                dead = 1
            me = True
        else:
            if count == 0 or not me:
                count +=1
            else:
                if count > 4:
                    score = 10000
                    return score
                if dead != 1:
                    score += int(10**(count-2))
                count = 1
                dead = 1
            me = False
    if count != 0:
        if count > 4:
            if me:
                score = 10000
            else:
                score = -10000
            return score
        if dead != 1:
            if me:
                score += int(10**(count-2))
            else:
                score -= int(10**(count-2))
    return score

def getboardscore(board):
    # Return the score of the whole board
    # 
    score = 0
    for i in range(BOARD_SIZE):
        line = [EMPTY] * BOARD_SIZE
        for j in range(BOARD_SIZE):
            line[j] = board[i][j]
        score = score + getlinescore(line)
    for i in range(BOARD_SIZE):
        line = [EMPTY] * BOARD_SIZE
        for j in range(BOARD_SIZE):
            line[j] = board[j][i]
        score = score + getlinescore(line)
    for i in range(BOARD_SIZE):
        line = [EMPTY] * (i+1)
        for j in range(i+1):
            line[j] = board[j][BOARD_SIZE-i+j-1]
        score = score + getlinescore(line)
    for i in range(BOARD_SIZE-1):
        line = [EMPTY] * (i+1)
        for j in range(i+1):
            line[j] = board[BOARD_SIZE-i+j-1][j]
        score = score + getlinescore(line)
    for i in range(BOARD_SIZE):
        line = [EMPTY] * (i+1)
        for j in range(i+1):
            line[j] = board[j][i-j]
        score = score + getlinescore(line)
    for i in range(BOARD_SIZE-1):
        line = [EMPTY] * (i+1)
        for j in range(i+1):
            line[j] = board[BOARD_SIZE-j-1][BOARD_SIZE-i+j-1]
        score = score + getlinescore(line)
    return score

def hasnearbypoint(board, x, y):
    # return whether x, y has a non empty place nearby
    # only place having non empty place nearby are marked as candidate
    if (x!= 0 and board[x-1][y] != EMPTY):
        return True
    if (x!=0 and y!=0 and board[x-1][y-1] != EMPTY):
        return True
    if (x!=0 and y!=BOARD_SIZE-1 and board[x-1][y+1] != EMPTY):
        return True
    if (y!=0 and board[x][y-1] != EMPTY):
        return True
    if (y!=BOARD_SIZE-1 and board[x][y+1] != EMPTY):
        return True
    if (x!=BOARD_SIZE-1 and board[x+1][y] != EMPTY):
        return True
    if (x!=BOARD_SIZE-1 and y!=0 and board[x+1][y-1] != EMPTY):
        return True
    if (x!=BOARD_SIZE-1 and y!=BOARD_SIZE-1 and board[x+1][y+1] != EMPTY):
        return True
    return False

def evaluatepoint(board, position, player):
    # evalute the score change (of player) if player play at position
    # assume position is valid
    change = 0
    [x, y] = position
    for k in range(2):
        score = 0
        line = [EMPTY] * BOARD_SIZE
        for i in range(BOARD_SIZE):
            line[i] = board[x][i]
        score += getlinescore(line)
        for i in range(BOARD_SIZE):
            line[i] = board[i][y]
        score += getlinescore(line)
        if (x + y < BOARD_SIZE):
            line = [EMPTY] * (x+y+1)
            for i in range(x+y+1):
                line[i] = board[i][x+y-i]
            score += getlinescore(line)
        else:
            line = [EMPTY] * (BOARD_SIZE*2-x-y-1)
            for i in range(BOARD_SIZE*2-x-y-1):
                line[i] = board[x+y+i+1-BOARD_SIZE][BOARD_SIZE-i-1]
            score += getlinescore(line)
        if (x > y):
            line = [EMPTY] * (BOARD_SIZE-x+y)
            for i in range(BOARD_SIZE-x+y):
                line[i] = board[i+x-y][i]
            score += getlinescore(line)
        else:
            line = [EMPTY] * (BOARD_SIZE-y+x)
            for i in range(BOARD_SIZE-y+x):
                line[i] = board[i][i+y-x]
            score += getlinescore(line)
        if (k == 0):
            change = change - score
            board[x][y] = player
        else:
            change = change + score
            board[x][y] = EMPTY
    return change

def getpossibleposition(board, player):
    # get all candidate places for playing
    # candidate place:
        #1. has non-empty place nearby
        #2. after playing, the score instatly go higher
    # return a list of [[pos_x, pos_y] , score_change]
    possible = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if (board[i][j] == EMPTY and hasnearbypoint(board, i, j)):
                change = evaluatepoint(board, [i, j], player)
                if ((player == ME and change > 0) or (player == OTHER and change < 0)):
                    possible.append([[i, j], change])
    return possible

class Node:
    # class of search tree node
    def __init__(self, place):
        self.height = None      # distance to root
        self.score = None       # score
        self.place = place      # position at board
        self.parent = None      # parent
        self.child = []         # children
        self.alpha = None       # alpha - beta value

class MinMaxTree:
    # class of search tree
    def __init__(self):
        self.root = Node(None)
        self.root.height = 0
        self.root.alpha = -50000

    def reconstruct(self):
        self.root = Node(None)
        self.root.height = 0
        self.root.alpha = -50000

    def insert(self, node, place, change):
        # insert a new node as child of node
        # change: score change compared with score of node
        newChild = Node(place)
        newChild.parent = node
        newChild.height = node.height + 1
        newChild.score = node.score + change
        if (newChild.height % 2 == 0):
            newChild.alpha = -50000
        else:
            newChild.alpha = 50000
        node.child.append(newChild)

    def deepsearch(self, node, board):
        # deep search code (alpha-beta cutting)
        # reference: https://github.com/lihongxun945/myblog/labels/五子棋AI教程第二版
        place = node.place
        height = node.height
        if height < 4:
            if (height % 2 == 1):
                board[place[0]][place[1]] = ME
                possible = getpossibleposition(board, OTHER)
                reverse = False
            else:
                board[place[0]][place[1]] = OTHER
                possible = getpossibleposition(board, ME)
                reverse = True
            for position, change in possible:
                self.insert(node, position, change)
            # sorting makes alpha-beta cutting more efficient
            node.child.sort(key = lambda s:s.score, reverse=reverse)
            # only choose 10 best places to consider (JOJ has 5s runtime fail)
            # this value should be adjusted..
            if (len(node.child) > 10):
                node.child = node.child[0:10]
            node.score = None
            scorelist = []
            for childnode in node.child:
                alpha = node.parent.alpha
                self.deepsearch(childnode, board)
                if (node.height%2 == 1):
                    # opponent choose
                    if (childnode.score < alpha):
                        node.score = childnode.score
                        break
                    else:
                        scorelist.append(childnode.score)
                else:
                    # I choose:
                    if (childnode.score > alpha):
                        node.score = childnode.score
                        break
                    else:
                        scorelist.append(childnode.score)
            # set alpha-beta value
            if (node.height%2 == 1):
                if (node.score == None):
                    node.score = min(scorelist)
                if (node.score > alpha):
                    node.parent.alpha = node.score
            else:
                if (node.score == None):
                    node.score = max(scorelist)
                if (node.score < alpha):
                    node.parent.alpha = node.score
            # set board back to origianl status (since not deep copy)
            board[place[0]][place[1]] = EMPTY

    def choice(self):
        # select best child of root and return its position
        maxscore = self.root.child[0].score
        bestplay = self.root.child[0].place
        for childnode in self.root.child:
            if (childnode.score > maxscore):
                maxscore = childnode.score
                bestplay = childnode.place
        return bestplay[0], bestplay[1]

class AI:
    boardSize = BOARD_SIZE;
    # TODO: add your own attributes here if you need any


    # Constructor
    def __init__(self):
        self.board = []
        for i in range(0,BOARD_SIZE):
            self.board.append([])
            for j in range(0,BOARD_SIZE):
                self.board[i].append(EMPTY)
        # TODO: add your own contructing procedure here if necessary
        self.tree = MinMaxTree()

    def init(self):
        # TODO: add your own initilization here if you need any
        self.tree = MinMaxTree()

    def begin(self):
        # TODO: write your own opening here
        # NOTE: this method is only called when it's your turn to begin (先手)
        # RETURN: two integer represent the axis of target position

        # issue regarding to 禁手 missing
        # should be considered in this function
        return self.turn()

    def turn(self):
        # TODO: write your in-turn operation here
        # NOTE: this method is called when it's your turn to put chess
        # RETURN: two integer represent the axis of target position

        self.tree.reconstruct()
        self.tree.root.score = getboardscore(self.board)
        possible = getpossibleposition(self.board, ME)
        for position, change in possible:
            self.tree.insert(self.tree.root, position, change)
        self.tree.root.child.sort(key = lambda s:s.score, reverse = True)
        if (len(self.tree.root.child)>20):
            self.tree.root.child = self.tree.root.child[0:20]
        for child in self.tree.root.child:
            self.tree.deepsearch(child, self.board)
        return self.tree.choice()

    @classmethod
    # NOTE: don't change this function
    def display(self):
        for i in range(0,BOARD_SIZE):
            print(self.board[i])

def loop(AI):
    # NOTE: don't change this function
    while True:
        buffer = input()
        buffersplitted = buffer.split(' ');
        if len(buffersplitted) == 0:
            continue
        command = buffersplitted[0]
        if command == START:
            AI.init();
        elif command == PLACE:
            x = int(buffersplitted[1])
            y = int(buffersplitted[2])
            v = int(buffersplitted[3])
            AI.board[x][y] = v
        elif command == DONE:
            print("OK")
        elif command == BEGIN:
            x, y = AI.begin()
            AI.board[x][y] = ME
            print(str(x)+" "+str(y))
        elif command == TURN:
            x = int(buffersplitted[1])
            y = int(buffersplitted[2])
            AI.board[x][y] = OTHER
            x, y = AI.turn()
            AI.board[x][y] = ME
            print(str(x)+" "+str(y))
        elif command == "print":
           AI.display()
        elif command == END:
            break

if __name__ == "__main__":
    # NOTE: don't change main function
    ai = AI()
    loop(ai)