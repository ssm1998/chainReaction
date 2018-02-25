print """Chain Reaction
This program is the logic behind the game of chain reaction. The GUI version i.e. game.py implements 
the pygame version."""
#A 9X6 Grid-Matrix, grid specifies the number of atoms present at a particular position
grid = [[0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0]]

#A 9X6 Grid-Matrix, colorGrid specifies the player number at a particular position
colorGrid = [[0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0],
             [0,0,0,0,0,0]]

"""Though a constant matrix is used, the program is not hardcoded. For the same reason, iteration through
   the matrix(grid) doesn't take any fixed range.
   The constant matrix is makes the pygame implementation much easier."""

play = raw_input("Do you want to play ? (y/n)")
players = input("Enter number of players: ")
playerList = range(1,players+1)
playerNum = 0
playerDict = {1: 'b',2: 'r',3: 'g',4: 'y'}

def printCombinedGrid(colorGrid,grid):
        rows = len(colorGrid)
        cols = len(colorGrid[0])
        print "  0  1  2  3  4  5"
        for row in range(rows):
                print row,
                for col in range(cols):
                        if colorGrid[row][col] != 0:
                                print str(grid[row][col])+playerDict[colorGrid[row][col]],
                        else:
                                print '0 ',
                print
        print

def multiPlayer():
        global playerList, playerNum
        while len(playerList) != 1:
                player = playerList[playerNum]
                print "Player " + str(player) + "'s turn !"
                x,y = input("Enter coordinate to place atom :")
                while( x > (len(grid)-1) or x < 0 or y > (len(grid[0])-1) or y < 0):
                        print("Index not available !")
                        x,y = input("Enter coordinate to place atom again :")
                addAtom((x,y), player)
                winCondition(colorGrid)

def playersOnBoard(colorGrid):
        rows = len(colorGrid)
        cols = len(colorGrid[0])
        mayWin = []
        for row in range(rows):
                for col in range(cols):
                        if colorGrid[row][col] != 0:
                                mayWin.append(colorGrid[row][col])
        return mayWin 

def winCondition(colorGrid):
        global playerList, playerNum
        mayWin = playersOnBoard(colorGrid)
        if (len(set(mayWin)) != len(playerList)):
                playerList = list(set(mayWin))
        if (len(set(mayWin)) == 1) and (len(mayWin) != 1):
                print "Congrats!!! Player " + str(mayWin[0]) + " you won :)"
                exit()
        playerNum += 1
        if playerNum > len(playerList)-1:
                playerNum = 0

def printGrid(grid):
        rows = len(grid)
        cols = len(grid[0])
        for row in range(rows):
                for col in range(cols):
                        print grid[row][col],
                print
        print

def checkGrids(grid, colorGrid):
        """Just prinitng both the martices in order to check whether the game works 
        fine or not"""
        print "This is total atoms grid"
        printGrid(grid)
        print "This is the player grid"
        printGrid(colorGrid)

def addNewAtom(grid, colorGrid, coordinate, player):
        x,y = coordinate
        for var in [(-1,0),(1,0),(0,-1),(0,1)]:
                if x+var[0] >= 0 and y+var[1] >= 0:
                        try:
                                grid[x+var[0]][y+var[1]] += 1
                                grid[x][y] = 0
                                colorGrid[x+var[0]][y+var[1]] = player
                                colorGrid[x][y] = 0
                                checkBurst(player)
                        except: pass
        printCombinedGrid(colorGrid,grid)

def checkBurst(player):
        rows = len(grid)
        cols = len(grid[0])
        cornerCells = [(0,0),(0,cols-1),(rows-1,0),(rows-1,cols-1)]
        edgeCells = [(0,x) for x in range(1,cols-1)]
        edgeCells += [(rows-1,x) for x in range(1,cols-1)]
        edgeCells += [(x,0) for x in range(1,rows-1)]
        edgeCells += [(x,cols-1) for x in range(1,rows-1)]
        restCells = []
        for row in range(rows):
                for col in range(cols):
                        restCells.append((row,col))
        restCells = set(restCells)
        restCells = restCells.difference(set(edgeCells))
        restCells = restCells.difference(set(cornerCells))
        for x,y in cornerCells:
                if grid[x][y] > 1:
                        print "burst"
                        addNewAtom(grid, colorGrid, (x,y), player)
        for x,y in edgeCells:
                if grid[x][y] > 2:
                        print "burst"
                        addNewAtom(grid, colorGrid, (x,y), player)
        for x,y in restCells:
                if grid[x][y] > 3:
                        print "burst"
                        addNewAtom(grid, colorGrid, (x,y), player)

def addAtom(coordinate, player):
        x,y = coordinate
        if grid[x][y] == 0:
                grid[x][y] += 1
                colorGrid[x][y] = player
                printCombinedGrid(colorGrid,grid)
        else:
                if colorGrid[x][y] == player:
                        grid[x][y] += 1
                        checkBurst(player)
                        printCombinedGrid(colorGrid,grid)
                else:
                        print "You are adding atom at the wrong place! "
                        print "Player " + str(player) + "'s turn !"
                        x,y = input("Enter coordinate to place atom :")
                        addAtom((x,y), player)

for player in playerList:
        print "Player " + str(player) + "'s turn !"
        x,y = input("Enter coordinate to place atom :")
        while( x > (len(grid)-1) or x < 0 or y > (len(grid[0])-1) or y < 0):
                print("Index not available !")
                x,y = input("Enter coordinate to place atom again :")
        addAtom((x,y), player)

while play == 'y':
        multiPlayer()
