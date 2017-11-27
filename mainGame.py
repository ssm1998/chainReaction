"""This is a second approach to CHAIN-REACTION which uses the concept of OOP for better implementation of pygame"""
import pygame, sys
from math import *

"""A strategy game for 2 to 8 players.

The objective of Chain Reaction is to take control of the board by eliminating your opponents' atoms.

Players take it in turns to place their atoms in a cell. Once a cell has reached critical mass the atoms
explode into the surrounding cells adding an extra orb and claiming the cell for the player. A player 
may only place their atoms in a blank cell or a cell that contains atoms of their own colour. As soon as
a player looses all their atoms they are out of the game.
"""

#Initializing pygame
pygame.init()

width = 600
height = 900

gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("CHAIN REACTION")
font = pygame.font.SysFont("Times New Roman", 60)
font2 = pygame.font.SysFont("Times New Roman", 40)
img = pygame.image.load("img.jpg")
img = pygame.transform.rotate(img, 90)
FPS1 = 20
FPS2 = 60
fpsClock = pygame.time.Clock()

#Colors     R    G    B
black  = (   0,   0,   0)  #Background color
color2 = ( 208, 211, 212)  #Border color
red    = ( 209,   0,   0)
white  = ( 244, 246, 247)
blue   = (  50,  36, 153)
blue2  = (   0, 255, 255)
violet = ( 151,  22, 191)
orange = ( 243, 160,  35)
yellow = ( 240, 255,  97)
green  = (  88, 214, 141)
pink   = ( 255,   0, 127)

#A dictionary with tuple values as key and respective strings as values 
totalPlayerDict = {red:'red', blue:'blue', orange:'orange', violet:'violet', yellow:'yellow', green:'green', pink:'pink', blue2:'blue2'}
players = [red, blue, orange, violet, yellow, green, pink, blue2]
playerDict = {} #A temporary game dictionary for the current players

blockSize = 100
noOfPlayers = 0             #Current number of players will be updated in this variable
noOfPlayers1 = noOfPlayers  #Temporary current number of players will be updated in this variable
atomsOfPlayers = []         #Numberof atoms of eachplayer has will be updated in this list
playerList = []             #Current players will be updated in this list
count = 0
d = blockSize/2 - 2         #Vibration constant

cols = width/blockSize
rows = height/blockSize

grid = [[0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0]]

def check():
        """ This definition is only for checking whether everything is fine"""
        print "No of players :", noOfPlayers
        print "PlayerList :", playerList
        print "Atoms Of Players :", atomsOfPlayers

def close():
        """It will close the game window"""
        pygame.quit()
        sys.exit()

class Cell:
        """This will create objects for each cell present in the grid"""
        def __init__(self):
                self.color = color2
                self.neighbours = []
                self.noOfAtoms = 0

        def addNeighbours(self, i, j):
                if i > 0:
                        self.neighbours.append(grid[i - 1][j])
                if i < rows - 1:
                        self.neighbours.append(grid[i + 1][j])
                if j > 0:
                        self.neighbours.append(grid[i][j - 1])
                if j < cols - 1:
                        self.neighbours.append(grid[i][j + 1])

def initializeGrid():
        """Initalizing everything"""
        global grid, atomsOfPlayers, playerList, playerDict
        grid = [[0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0]]
        atomsOfPlayers = []
        for atom in range(noOfPlayers):
                atomsOfPlayers.append(0)

        playerList = []
        for player in range(noOfPlayers):
                playerList.append(players[player])
                playerDict[players[player]] = totalPlayerDict[players[player]]

        for row in range(rows):
                for col in range(cols):
                        grid[row][col] = Cell()

        for row in range(rows):
                for col in range(cols):
                        grid[row][col].addNeighbours(row,col)

def drawGrid(currentPlayer):
        """Drawing grids for respective players, according to their turn.
           The color of the grid will show which player's turn it will be."""
        global playerList, noOfPlayers, players
        row = 0
        col = 0
        for var in range(height/blockSize):
                row += blockSize
                col += blockSize
                pygame.draw.line(gameDisplay, playerList[currentPlayer], (col, 0), (col, height))
                pygame.draw.line(gameDisplay, playerList[currentPlayer], (0, row), (width, row))

def showPresentGrid(vibrate = 1):
        """This will draw the atoms as per the game proceeds"""
        r = -blockSize
        c = -blockSize
        for i in range(rows):
                r = -blockSize
                c += blockSize 
                for j in range(cols):
                        r += blockSize
                        if grid[i][j].noOfAtoms == 0:
                                grid[i][j].color = color2
                        elif grid[i][j].noOfAtoms == 1:
                                pygame.draw.ellipse(gameDisplay, grid[i][j].color, (r + blockSize/2 - d/2 + vibrate, c + blockSize/2 - d/2, d, d))
                        elif grid[i][j].noOfAtoms == 2:
                                pygame.draw.ellipse(gameDisplay, grid[i][j].color, (r + 5, c + blockSize/2 - d/2 - vibrate, d, d))
                                pygame.draw.ellipse(gameDisplay, grid[i][j].color, (r + d/2 + blockSize/2 - d/2 + vibrate, c + blockSize/2 - d/2, d, d))
                        elif grid[i][j].noOfAtoms == 3:
                                angle = 90
                                x = r + (d/2)*cos(radians(angle)) + blockSize/2 - d/2
                                y = c + (d/2)*sin(radians(angle)) + blockSize/2 - d/2
                                pygame.draw.ellipse(gameDisplay, grid[i][j].color, (x - vibrate, y, d, d))
                                x = r + (d/2)*cos(radians(angle + 90)) + blockSize/2 - d/2
                                y = c + (d/2)*sin(radians(angle + 90)) + 5
                                pygame.draw.ellipse(gameDisplay, grid[i][j].color, (x + vibrate, y, d, d))
                                x = r + (d/2)*cos(radians(angle - 90)) + blockSize/2 - d/2
                                y = c + (d/2)*sin(radians(angle - 90)) + 5
                                pygame.draw.ellipse(gameDisplay, grid[i][j].color, (x - vibrate, y, d, d))

        pygame.display.flip()

def addAtom(i, j, color):
        """Whenever the player clicks, it adds atom to the cell(if possible)"""
        grid[i][j].noOfAtoms += 1
        grid[i][j].color = color
        if grid[i][j].noOfAtoms >= len(grid[i][j].neighbours):
                checkBurst(grid[i][j], color)

def checkBurst(cell, color):
        showPresentGrid()
        cell.noOfAtoms = 0
        for n in range(len(cell.neighbours)):
                cell.neighbours[n].noOfAtoms += 1
                cell.neighbours[n].color = color
                if cell.neighbours[n].noOfAtoms >= len(cell.neighbours[n].neighbours):
                        checkBurst(cell.neighbours[n], color)

def isPlayerInGame():
        """This updates the atoms of each player in the atomsOfPlayers list"""
        global atomsOfPlayers, playerList
        playerAtom = []
        for _ in range(noOfPlayers):
                playerAtom.append(0)
        for row in range(rows):
                for col in range(cols):
                        for player in range(noOfPlayers):
                                if grid[row][col].color == playerList[player]:
                                        playerAtom[player] += grid[row][col].noOfAtoms
        atomsOfPlayers = playerAtom[:]

def gameOver(player):
        """Will end the game, if player wins"""
        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                close()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                        close()
                                if event.key == pygame.K_r:
                                        startGame()

                text = font.render("Player %s Won!" % playerDict[player], True, white)
                text2 = font.render("Press \'r\' to Reset!", True, white)
                text3 = font.render("Press \'q\' to Quit!", True, white)

                gameDisplay.blit(text, (width/5, height/4))
                gameDisplay.blit(text2, (width/5, height/3))
                gameDisplay.blit(text3, (width/5, height/2))

                pygame.display.flip()
                fpsClock.tick(FPS2)

def checkWin():
        """Checks which player wins"""
        global playerList, noOfPlayers, atomsOfPlayers, noOfPlayers1, playerDict
        zeroPlayer = 0  #number of players whose atoms are zero.
        temp = atomsOfPlayers[:]
        for player in range(len(playerList)):
                if atomsOfPlayers[player] == 0:
                        zeroPlayer += 1
                        try:
                                playerDict.pop(playerList.pop(player))
                                temp.pop(player)
                                noOfPlayers1 = len(playerList)
                        except :pass
        if zeroPlayer == noOfPlayers - 1:
                for player in range(len(playerList)):
                        if atomsOfPlayers[player]:
                                return playerList[player]
        atomsOfPlayers = temp
        noOfPlayers = noOfPlayers1

def startGame():
        global noOfPlayers, noOfPlayers1, count
        count = 0
        noOfPlayers = 0
        gameDisplay.fill(black)
        gameDisplay.blit(img, (width/2, height/2))
        text = font2.render("Welcome to CHAIN REACTION", True, white)
        text2 = font2.render("Press 2,3,4,5,6,7 or 8", True, white)
        text3 = font2.render("for respective player game", True, white)
        text4 = font2.render("Press \'q\' to quit!", True, white)

        gameDisplay.blit(text, (width/20, height/5))
        gameDisplay.blit(text2, (width/8, height/4))
        gameDisplay.blit(text3, (width/8, int(height/3.3)))
        gameDisplay.blit(text4, (width/8, height/2))
        while True:
                if noOfPlayers != 0:
                        break
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                close()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                        close()
                                elif event.key == pygame.K_2:
                                        noOfPlayers = 2
                                        noOfPlayers1 = noOfPlayers
                                elif event.key == pygame.K_3:
                                        noOfPlayers = 3
                                        noOfPlayers1 = noOfPlayers
                                elif event.key == pygame.K_4:
                                        noOfPlayers = 4
                                        noOfPlayers1 = noOfPlayers
                                elif event.key == pygame.K_5:
                                        noOfPlayers = 5
                                        noOfPlayers1 = noOfPlayers
                                elif event.key == pygame.K_6:
                                        noOfPlayers = 6
                                        noOfPlayers1 = noOfPlayers
                                elif event.key == pygame.K_7:
                                        noOfPlayers = 7
                                        noOfPlayers1 = noOfPlayers
                                elif event.key == pygame.K_8:
                                        noOfPlayers = 8
                                        noOfPlayers1 = noOfPlayers
                pygame.display.flip()
                fpsClock.tick(FPS1)
        gameLoop()


def gameLoop():
        global count, noOfPlayers, playerList, playerDict
        initializeGrid()

        turns = 0
        
        currentPlayer = 0

        vibrate = 0.5

        while True:
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                close()
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                        close()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                x, y = pygame.mouse.get_pos()
                                i = y/blockSize
                                j = x/blockSize
                                if grid[i][j].color == playerList[currentPlayer] or grid[i][j].color == color2:
                                        turns += 1
                                        addAtom(i, j, playerList[currentPlayer])
                                        currentPlayer += 1
                                        if currentPlayer >= noOfPlayers:
                                                currentPlayer = 0
                                        if turns >= noOfPlayers:
                                                isPlayerInGame()

                                count += 1
                
                gameDisplay.fill(black)
                
                vibrate *= -1 # Vibrating the Atoms
                
                try:
                        drawGrid(currentPlayer)
                except: 
                        currentPlayer = 0
                showPresentGrid(vibrate)
                
                pygame.display.flip()

                if count > noOfPlayers:
                        winner = checkWin()
                        if winner != None:
                                gameOver(winner)

                fpsClock.tick(FPS1)

startGame()

