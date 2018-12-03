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

def match(list1, list2):
    # return a list containing place list2 appear in list1
    # return empty list if not found
    place = []
    if (len(list1) < len(list2)):
        return place
    for i in range(len(list1) - len(list2) + 1):
        flag = True
        for j in range(len(list2)):
            if list1[i+j] != list2[j]:
                flag = False
                break
        if flag:
            place.append(i)
    return place

def checknumempty(shape):
    count = 0
    for i in range(len(shape)):
        if shape[i] == EMPTY:
            count = count + 1
    return count

def checknumme(shape, direction):
    count = 0
    if direction == 1:
        for i in range(len(shape)):
            if shape[i] == ME:
                count = count + 1
        return count
    else:
        length = len(shape)
        for i in range(length):
            if shape[length - i - 1] == ME:
                count = count + 1
        return count

def restrip(shape):
    i = 0
    while i<len(shape) and shape[i] == EMPTY:
        i = i + 1
    shape = shape[i:]
    i = len(shape) - 1
    while i>=0 and shape[i] == EMPTY:
        i = i - 1
    shape = shape[0:i+1]
    return shape

def getshapescore(shape):
    space = 0
    length = len(shape)
    if length == 0:
        return 0
    if shape[0] == EMPTY:
        leftEmpty = True
        space = space + 1
    else:
        leftEmpty = False
    if shape[length-1] == EMPTY:
        rightEmpty = True
        space = space + 1
    else:
        rightEmpty = False
    shape = restrip(shape)
    length = len(shape)
    numEmpty = checknumempty(shape)
    if length == 0 or length == 1:
        return 0
    if length == 2:
        if space == 0 or space == 1:
            return 0
        else:
            return 10
    if length == 3:
        if numEmpty == 1:
            if space == 0 or space ==1:
                return 0
            else:
                return 10
        else:
            if space == 0:
                return 0
            elif space == 1:
                return 10
            else:
                return 100
    if length == 4:
        if numEmpty == 2:
            if space == 0 or space == 1:
                return 0
            else:
                return 10
        if numEmpty == 1:
            if space == 0:
                return 0
            elif space == 1:
                return 10
            else:
                return 100
        else:
            if space == 0:
                return 0
            elif space == 1:
                return 100
            else:
                return 1000
    if length == 5:
        if numEmpty == 3:
            return 0
        elif numEmpty == 2:
            return 10
        elif numEmpty == 1:
            return 100
        else:
            return 10000
    if length == 6:
        if numEmpty == 0:
            return 10000
        numMeLeft = checknumme(shape, 1)
        numMeRight = checknumme(shape, 2)
        if (leftEmpty and numMeLeft == 4) or (rightEmpty and numMeRight == 4):
            return 1000
        if (leftEmpty and numMeLeft == 3) or (rightEmpty and numMeRight == 3):
            return 100
        elif numEmpty < 3:
            return 10
        else:
            return 0
    if length >=7:
        count = 0
        numMeLeft = checknumme(shape, 1)
        numMeRight = checknumme(shape, 2)
        if (len(match(shape, [ME, ME, ME, ME, ME]))>0):
            return 10000
        if (leftEmpty and numMeLeft == 4) or (rightEmpty and numMeRight == 4) or (len(match(shape, [EMPTY, ME, ME, ME, ME, EMPTY]))>0):
            return 1000
        if (leftEmpty and numMeLeft == 3) :
            count = count + 1
        if (rightEmpty and numMeRight == 3):
            count = count + 1
        count = count + len([match(shape, [EMPTY, ME, ME, ME, EMPTY]), match(shape, [EMPTY, ME, EMPTY, ME, ME, EMPTY]), match(shape, [EMPTY, ME, ME, EMPTY, ME, EMPTY])])
        return count*100

def getlinescore(line):
    score = 0
    length = len(line)
    prev = -1
    for i in range(length):
        if line[i] == OTHER:
            shape = line[prev+1:i]
            score = score + getshapescore(shape)
            prev = i
    shape = line[prev+1:]
    score = score + getshapescore(shape)
    return score

def getlinetotal(line):
    score = getlinescore(line)
    for i in range(len(line)):
        if line[i] == ME:
            line[i] = OTHER
        elif line[i] == OTHER:
            line[i] = ME
    score = score - getlinescore(line)
    return score

def getboardscore(board):
    score = 0
    for i in range(BOARD_SIZE):
        line = [EMPTY] * BOARD_SIZE
        for j in range(BOARD_SIZE):
            line[j] = board[i][j]
        score = score + getlinetotal(line)
    for i in range(BOARD_SIZE):
        line = [EMPTY] * BOARD_SIZE
        for j in range(BOARD_SIZE):
            line[j] = board[j][i]
        score = score + getlinetotal(line)
    for i in range(BOARD_SIZE):
        line = [EMPTY] * (i+1)
        for j in range(i+1):
            line[j] = board[j][BOARD_SIZE-i+j-1]
        score = score + getlinetotal(line)
    for i in range(BOARD_SIZE-1):
        line = [EMPTY] * (i+1)
        for j in range(i+1):
            line[j] = board[BOARD_SIZE-i+j-1][j]
        score = score + getlinetotal(line)
    for i in range(BOARD_SIZE):
        line = [EMPTY] * (i+1)
        for j in range(i+1):
            line[j] = board[j][i-j]
        score = score + getlinetotal(line)
    for i in range(BOARD_SIZE-1):
        line = [EMPTY] * (i+1)
        for j in range(i+1):
            line[j] = board[BOARD_SIZE-j-1][BOARD_SIZE-i+j-1]
        score = score + getlinetotal(line)
    return score

def hasnearbypoint(board, x, y):
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
    # evalute the score (of player) change if player play at position
    # assume position is valid
    change = 0
    [x, y] = position
    for k in range(2):
        score = 0
        line = [EMPTY] * BOARD_SIZE
        for i in range(BOARD_SIZE):
            line[i] = board[x][i]
        score += getlinetotal(line)
        for i in range(BOARD_SIZE):
            line[i] = board[i][y]
        score += getlinetotal(line)
        if (x + y < BOARD_SIZE):
            line = [EMPTY] * (x+y+1)
            for i in range(x+y+1):
                line[i] = board[i][x+y-i]
            score += getlinetotal(line)
        else:
            line = [EMPTY] * (BOARD_SIZE*2-x-y-1)
            for i in range(BOARD_SIZE*2-x-y-1):
                line[i] = board[x+y+i+1-BOARD_SIZE][BOARD_SIZE-i-1]
            score += getlinetotal(line)
        if (x > y):
            line = [EMPTY] * (BOARD_SIZE-x+y)
            for i in range(BOARD_SIZE-x+y):
                line[i] = board[i+x-y][i]
            score += getlinetotal(line)
        else:
            line = [EMPTY] * (BOARD_SIZE-y+x)
            for i in range(BOARD_SIZE-y+x):
                line[i] = board[i][i+y-x]
            score += getlinetotal(line)
        if (k == 0):
            change = change - score
            board[x][y] = player
        else:
            change = change + score
            board[x][y] = EMPTY
    return change

def getpossibleposition(board, player):
    possible = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if (board[i][j] == EMPTY and hasnearbypoint(board, i, j)):
                change = evaluatepoint(board, [i, j], player)
                if ((player == ME and change > 0) or (player == OTHER and change < 0)):
                    possible.append([[i, j], change])
    return possible

class MinMaxTree:
    def __init__(self):
        self.root = Node(None)
        self.root.degree = 0
        self.root.alpha = -50000

    def reconstruct(self):
        self.root = Node(None)
        self.root.degree = 0
        self.root.alpha = -50000

    def insert(self, node, place, change):
        newChild = Node(place)
        newChild.parent = node
        newChild.degree = node.degree + 1
        newChild.score = node.score + change
        if (newChild.degree % 2 == 0):
            newChild.alpha = -50000
        else:
            newChild.alpha = 50000
        node.child.append(newChild)

    def deepsearch(self, node, board):
        place = node.place
        degree = node.degree
        if degree < 2:
            if (degree % 2 == 1):
                board[place[0]][place[1]] = ME
                possible = getpossibleposition(board, OTHER)
                reverse = False
            else:
                board[place[0]][place[1]] = OTHER
                possible = getpossibleposition(board, ME)
                reverse = True
            for position, change in possible:
                self.insert(node, position, change)
            node.child.sort(key = lambda s:s.score, reverse=reverse)
            node.score = None
            scorelist = []
            for childnode in node.child:
                alpha = node.parent.alpha
                self.deepsearch(childnode, board)
                if (node.degree%2 == 1):
                    # opponent choose
                    if (childnode.score < alpha):
                        node.score = childnode.score
                        break
                    else:
                        scorelist.append(childnode.score)
                else:
                    # me choose:
                    if (childnode.score > alpha):
                        node.score = childnode.score
                        break
                    else:
                        scorelist.append(childnode.score)
            if (node.degree%2 == 1):
                if (node.score == None):
                    node.score = min(scorelist)
                if (node.score > alpha):
                    node.parent.alpha = node.score
            else:
                if (node.score == None):
                    node.score = max(scorelist)
                if (node.score < alpha):
                    node.parent.alpha = node.score
            board[place[0]][place[1]] = EMPTY

    def choice(self):
        maxscore = self.root.child[0].score
        bestplay = self.root.child[0].place
        for childnode in self.root.child:
            if (childnode.score > maxscore):
                maxscore = childnode.score
                bestplay = childnode.place
        return bestplay[0], bestplay[1]

class Node:
    def __init__(self, place):
        self.degree = None
        self.score = None
        self.place = place
        self.parent = None
        self.child = []
        self.alpha = None

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
        # The following one is a very naive sample which always put chess at the first empty slot.
        return self.turn()

    def turn(self):
        # TODO: write your in-turn operation here
        # NOTE: this method is called when it's your turn to put chess
        # RETURN: two integer represent the axis of target position
        # The following one is a very naive sample which always put chess at the first empty slot.
        self.tree.reconstruct()
        self.tree.root.score = getboardscore(self.board)
        possible = getpossibleposition(self.board, ME)
        for position, change in possible:
            self.tree.insert(self.tree.root, position, change)
        self.tree.root.child.sort(key = lambda s:s.score, reverse = True)
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