import random
import sys
import re

BLOCKCHAR = '#' # blocked square (black square)
OPENCHAR = '-' # open square (not decided yet)
PROTECTEDCHAR = '~' # Reserved for word characters


def create_Board(x, y):
    board = []
    for i in range(x):
        board.append([0] * y)
    for i in range(len(board)):
        for j in range(len(board[0])):
            board[i][j] = OPENCHAR
    symmetry(board, BLOCKCHAR)
    mandatory(board)
    return board

def insertBlocks(board, x, y):
    board[x][y] = BLOCKCHAR
    symmetry(board, BLOCKCHAR)
    mandatory(board)
    return board

def symmetry(board, char_type):
    indexes = []
    rows = len(board)
    cols = len(board[0])
    length = rows*cols - 1
    index = 0
    for i in range(rows):
        for j in range(cols):
            if(board[i][j] == char_type):
                indexes.append(index)
            index+=1
    for element in indexes:
        inverse = length - element
        new_x = int(inverse / cols)
        new_y =  inverse - (new_x * cols)
        if(board[new_x][new_y] == PROTECTEDCHAR):
            return False
        board[new_x][new_y] = char_type
    return True

def insert_horizontal(board, word, x, y):
    for char in word:
        board[x][y] = char
        y += 1
    return board

def insert_vertical(board, word, x, y):
    for char in word:
        board[x][y] = char
        x += 1
    return board

def switch(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] != OPENCHAR):
                if(board[i][j] != BLOCKCHAR):
                    board[i][j] = PROTECTEDCHAR
    symmetry(board, PROTECTEDCHAR)
    return board

def isValid(xpos, ypos, board):
    if(ypos-1 >=0 ):
        if(board[xpos][ypos-1] == PROTECTEDCHAR):
            return False
    if (ypos - 2 >= 0):
        if (board[xpos][ypos - 2] == PROTECTEDCHAR):
            return False
    if (ypos + 2 < len(board[0])):
        if (board[xpos][ypos +2] == PROTECTEDCHAR):
            return False
    if (ypos + 1 < len(board[0])):
        if (board[xpos][ypos +1] == PROTECTEDCHAR):
            return False
    if (xpos - 2 >= 0):
        if (board[xpos-2][ypos] == PROTECTEDCHAR):
            return False
    if (xpos - 1 >= 0):
        if (board[xpos-1][ypos] == PROTECTEDCHAR):
            return False
    if (xpos + 2 < len(board)):
        if (board[xpos+2][ypos] == PROTECTEDCHAR):
            return False
    if (xpos + 1 < len(board)):
        if (board[xpos+1][ypos] == PROTECTEDCHAR):
            return False
    return True

def mandatory(board):
    x = len(board) + 2
    y = len(board[1]) + 2
    temp = []
    for i in range(x):
        temp.append([0] * y)
    for i in range(len(temp)):
        for j in range(len(temp[0])):
            temp[i][j] = BLOCKCHAR
    for i in range(len(board)):
        for j in range(len(board[0])):
            temp[i+1][j+1] = board[i][j]

    for i in range(len(board)):
        for j in range(len(board[0])):
            if(temp[i+1][j+1] == BLOCKCHAR):
                if(j-2 >= 0):
                    if(temp[i+1][j-2] == BLOCKCHAR):
                        temp[i+1][j-1] = BLOCKCHAR
                if(j+4 < len(temp[0])):
                    if (temp[i+1][j+4] == BLOCKCHAR):
                        temp[i+1][j+3] = BLOCKCHAR
                if (i-2 >= 0):
                    if (temp[i-2][j+1] == BLOCKCHAR):
                        temp[i-1][j+1] = BLOCKCHAR
                if (i+4 < len(temp)):
                    if (temp[i+4][j+1] == BLOCKCHAR):
                        temp[i+3][j+1] = BLOCKCHAR
                if (j-1 >= 0):
                    if (temp[i+1][j-1] == BLOCKCHAR):
                        temp[i+1][j] = BLOCKCHAR
                if (j+3 < len(temp[0])):
                    if (temp[i+1][j+3] == BLOCKCHAR):
                        temp[i+1][j+2] = BLOCKCHAR
                if (i-1 >= 0):
                    if(temp[i-1][j+1] == BLOCKCHAR):
                        temp[i][j+1] = BLOCKCHAR
                if (i+3 < len(temp)):
                    if (temp[i+3][j+1] == BLOCKCHAR):
                        temp[i+2][j+1] = BLOCKCHAR

    for i in range(len(board)):
        for j in range(len(board[0])):
            board[i][j] = temp[i+1][j+1]
    return symmetry(board, BLOCKCHAR)

def format(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            print(board[i][j], end = " ")
        print()
    print()

def answer(board):
    result = ""
    for i in range(len(board)):
        for j in range(len(board[0])):
            result += board[i][j]
    return result

def count_blocks(board):
    count = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] == BLOCKCHAR):
                count += 1
    return count

def convert(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] ==PROTECTEDCHAR):
                board[i][j] = OPENCHAR
    return board

def fill_in(original, board, num):
    symmetry(board, BLOCKCHAR)
    mandatory(board)
    count = count_blocks(board)
    if(count == num):
        return board

    temp = []
    for i in range(len(board)):
        temp.append([0] * len(board[0]))
    for i in range(len(temp)):
        for j in range(len(temp[0])):
            temp[i][j] = board[i][j]

    x = 0
    y = 0
    can_break = False
    while(can_break == False):
        x = random.randint(0, len(board)-1)
        y = random.randint(0, len(board[0])-1)
        if(board[x][y] == OPENCHAR):
            if(isValid(x, y, board)):
                can_break = True
    temp[x][y] = BLOCKCHAR
    x = symmetry(temp, BLOCKCHAR)
    if(x == False):
        return fill_in(original, original, num)
    mandatory(temp)
    new_count = count_blocks(temp)
    if(new_count == num):
        result = []
        for i in range(len(temp)):
            result.append([0] * len(temp[0]))
        for i in range(len(result)):
            for j in range(len(result[0])):
                result[i][j] = temp[i][j]
        connect(result, 0, 0)
        if checkConnect(result):
            return temp
        return fill_in(original, original, num)
    elif(new_count > num):
        return fill_in(original, original, num)
    else:
        return fill_in(original, temp, num)

def connect(board, xpos, ypos):
    if(board[xpos][ypos] not in '#X'):
        board[xpos][ypos] = 'X'
        if(xpos+1 < len(board)):
            if(board[xpos+1][ypos] != BLOCKCHAR):
                connect(board, xpos+1, ypos)
        if (xpos-1 >= 0):
            if (board[xpos - 1][ypos] != BLOCKCHAR):
                connect(board, xpos - 1, ypos)
        if (ypos-1 >= 0):
            if (board[xpos][ypos - 1] != BLOCKCHAR):
                connect(board, xpos, ypos-1)
        if (ypos+1 < len(board[0])):
            if (board[xpos][ypos +1] != BLOCKCHAR):
                connect(board, xpos, ypos+1)
    return

def checkConnect(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] == OPENCHAR):
                return False
            if (board[i][j] == PROTECTEDCHAR):
                return False
    return True

def finish(result):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if (board[i][j] == PROTECTEDCHAR or board[i][j] == 'X'):
                board[i][j] = OPENCHAR
    return result

input = list(sys.argv)
input = input[1:]

dimensions = re.split('(\d+)', input[0].strip())
width = int(dimensions[3])
height = int(dimensions[1])
blocks = int(input[1])
dictionary = input[2]

board = create_Board(height, width)

for i in range(len(input)):
    if(i > 2):
        word = input[i]
        positions = re.split('(\d+)', word.strip())
        direction = positions[0].upper()
        xpos = int(positions[1])
        ypos = int(positions[3])
        letters = positions[4]
        if(letters == BLOCKCHAR):
            insertBlocks(board, xpos, ypos)
        if(direction == 'V'):
            insert_vertical(board, letters.upper(), xpos, ypos)
        else:
            insert_horizontal(board, letters.upper(), xpos, ypos)

switch(board)
if(blocks%2 == 1):
    insertBlocks(board, int(width/2), int(height/2))

result = fill_in(board, board, blocks)
finish(result)
convert(result)
format(result)
print(answer(result))
