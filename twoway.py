## Sobakan game for homework 6 ##

from tkinter import *
from tkinter.ttk import *
import math
import random as rand

def make2dList(rows, cols):
    # helper function to create a 2d list 
    a=[]
    for row in range(rows): a += [[0]*cols]
    return a

####################################
# customize these functions
####################################

class Person(object):
    def __init__(self):
        self.side = rand.randint(0, 1) #0 for top side, 1 for bottom side
        self.x = 0

def initSokoban(data):
    # load data.xyz as appropriate
    data.rows = 9 #the dimensions for level 1 on wikipedia
    data.cols = 8 
    data.board = make2dList(data.rows, data.cols)
    data.cellWidth = data.width/data.cols
    data.EMPTY = 0
    data.WALL = 1
    data.BOX = 2
    data.SPOT = 3
    data.PLAYER = 4
    data.BOXPLACED = 5
    initLevel1(data)
    data.gameWon = False
    data.curRow = 2
    data.curCol = 2
    data.board[data.curRow][data.curCol] = data.PLAYER #init position of player
    data.numOfBoxes = 7

def placeSpot(data, row, col):
    if data.board[row][col] != data.BOXPLACED: data.board[row][col] = data.SPOT

def initSpots1(data):
    row, col = 2, 1
    placeSpot(data, row, col)
    row, col = 4, 1
    placeSpot(data, row, col)
    row, col = 5, 4
    placeSpot(data, row, col)
    row, col = 7, 4
    placeSpot(data, row, col)
    row, col = 3, 5
    placeSpot(data, row, col)
    row, col = 6, 3
    placeSpot(data, row, col)
    row, col = 6, 6
    placeSpot(data, row, col)

def initBoxes1(data):
    data.board[2][3] = data.BOX
    data.board[3][4] = data.BOX
    data.board[4][4] = data.BOX
    data.board[6][1] = data.BOX
    data.board[6][3] = data.BOXPLACED
    data.board[6][4] = data.BOX
    data.board[6][5] = data.BOX

def initWalls1(data):
    for col in range(data.cols):
        data.board[0][col] = data.WALL
        data.board[-1][col] = data.WALL
    for row in range(data.rows):
        data.board[row][0] = data.WALL
        data.board[row][-1] = data.WALL
    data.board[1][1] = data.WALL
    data.board[1][2] = data.WALL
    data.board[3][1] = data.WALL
    data.board[3][2] = data.WALL
    data.board[4][2] = data.WALL
    data.board[4][3] = data.WALL
    data.board[5][2] = data.WALL
    for row in range(1, 6):
        data.board[row][6] = data.WALL

def initLevel1(data):
    initWalls1(data)
    initSpots1(data)
    initBoxes1(data)

def drawBoardSokoban(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            x0, y0 = data.cellWidth * col, data.cellWidth * row
            x1, y1 = data.cellWidth * (col+1), data.cellWidth * (row+1)
            if data.board[row][col] == data.WALL:
                canvas.create_rectangle(x0, y0, x1, y1, fill = "orange",
                    outline = "gold", width = 3)
            elif data.board[row][col] == data.BOX:
                canvas.create_rectangle(x0, y0, x1, y1, fill = "maroon")
            elif data.board[row][col] == data.BOXPLACED:
                canvas.create_rectangle(x0, y0, x1, y1, fill = "green")
            elif data.board[row][col] == data.SPOT:
                mod = data.cellWidth/4
                canvas.create_oval(x0+mod, y0+mod, x1-mod, y1-mod, fill = "red")
            elif data.board[row][col] == data.PLAYER:
                canvas.create_oval(x0, y0, x1, y1, fill = "light blue")

def moveBoxPlaced(data, oldRow, oldCol, newRow, newCol, drow, dcol):
    if data.board[newRow+drow][newCol+dcol] == data.EMPTY:
        data.board[newRow+drow][newCol+dcol] = data.BOX
        if data.board[newRow][newCol] != data.BOXPLACED: initSpots1(data)
        data.board[oldRow][oldCol] = data.EMPTY
        data.curRow, data.curCol = newRow, newCol
        data.board[newRow][newCol] = data.PLAYER
    elif data.board[newRow+drow][newCol+dcol] == data.SPOT:
        data.board[newRow+drow][newCol+dcol] = data.BOXPLACED
        data.board[oldRow][oldCol] = data.EMPTY
        data.curRow, data.curCol = newRow, newCol
        data.board[newRow][newCol] = data.PLAYER

def moveBox(data, oldRow, oldCol, newRow, newCol, drow, dcol):
    if data.board[newRow+drow][newCol+dcol] == data.EMPTY:
        data.board[newRow+drow][newCol+dcol] = data.BOX
        data.board[oldRow][oldCol] = data.EMPTY
        data.curRow, data.curCol = newRow, newCol
        data.board[newRow][newCol] = data.PLAYER
        if data.board[newRow][newCol] != data.BOXPLACED: initSpots1(data)
    elif data.board[newRow+drow][newCol+dcol] == data.SPOT:
        data.board[newRow+drow][newCol+dcol] = data.BOXPLACED
        data.board[oldRow][oldCol] = data.EMPTY
        data.curRow, data.curCol = newRow, newCol
        data.board[newRow][newCol] = data.PLAYER

def movePlayerSokoban(data, drow, dcol):
    oldRow = data.curRow
    oldCol = data.curCol
    newRow = data.curRow + drow
    newCol = data.curCol + dcol
    testPos = data.board[newRow][newCol]
    if testPos == data.EMPTY or testPos == data.SPOT:
        data.curRow, data.curCol = newRow, newCol
        data.board[oldRow][oldCol] = data.EMPTY #moves player into empty space
        if data.board[newRow][newCol] != data.BOXPLACED: initSpots1(data) 
        #makes the spots constant all the time
        data.board[newRow][newCol] = data.PLAYER
    elif data.board[newRow][newCol] == data.BOX:
        moveBox(data, oldRow, oldCol, newRow, newCol, drow, dcol)
    elif data.board[newRow][newCol] == data.BOXPLACED:
        moveBoxPlaced(data, oldRow, oldCol, newRow, newCol, drow, dcol)
    elif data.board[newRow][newCol] == data.WALL:
        pass #doesn't move player at all
    testGameWon(data)

def cheatSokoban(data, drow, dcol):
    newRow = data.curRow + drow
    newCol = data.curCol + dcol
    testPos = data.board[newRow][newCol]
    if testPos == data.WALL: data.board[newRow][newCol] = data.EMPTY

def drawGameWon(canvas, data):
    if data.gameWon == True:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "white")
        canvas.create_text(data.width/2, data.height/2, text = "You Won!!!!", 
            font = "Arial 30 bold", fill = "maroon")

def testGameWon(data):
    boxCount = 0
    for row in range(data.rows):
        for col in range(data.cols):
            if data.board[row][col] == data.BOXPLACED:
                boxCount += 1
    if boxCount == data.numOfBoxes: data.gameWon = True


def mousePressedSokoban(event, data):
    pass

def keyPressedSokoban(event, data):
    # use event.char and event.keysym
    if event.keysym == 'r': initSokoban(data)
    if data.gameWon == False:
        if event.keysym == 'Left': movePlayerSokoban(data, 0, -1)
        elif event.keysym == 'Right': movePlayerSokoban(data, 0, +1)
        elif event.keysym == 'Up': movePlayerSokoban(data, -1, 0)
        elif event.keysym == 'Down': movePlayerSokoban(data, +1, 0)
        elif event.keysym == 'a': cheatSokoban(data, 0, -1)
        elif event.keysym == 'd': cheatSokoban(data, 0, +1)
        elif event.keysym == 'w': cheatSokoban(data, -1, 0)
        elif event.keysym == 's': cheatSokoban(data, +1, 0)

def timerFiredSokoban(data):
    pass

def drawInstructions(canvas, data):
    helpText = "Press r to restart, arrow keys to move, WASD to cheat"
    canvas.create_text(data.width/2, data.height*19/20, text = helpText,
        font = "Arial 12")

def redrawTwoWay(canvas, data):
    canvas.create_rectangle(data.width/2, data.height/2, 
        data.width/2+100, data.height/2+100, fill = "maroon");

def redrawAllSokoban(canvas, data):
    drawBoardSokoban(canvas, data)
    drawInstructions(canvas, data)
    drawGameWon(canvas, data)

####################################
# use the run function as-is
####################################

def runTwoWay(width, height):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        # redrawAllSokoban(canvas, data)
        redrawTwoWay(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressedSokoban(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressedSokoban(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFiredSokoban(data)
        redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10000
    initSokoban(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    image = PhotoImage(file = "assets/singlepath_base.png")
    label = Label(image = image)
    label.place(x = 0, y = 0, relwidth = 1, relheight = 1)

    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed


width = 1152
height = 648
runTwoWay(width, height)
