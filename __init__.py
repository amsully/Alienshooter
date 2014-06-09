'''
Created on May 30, 2014

@author: Alex Sullivan
'''


'''
TESTING PULLING THE REPO.
'''

import pygame, sys
from pygame.locals import *
from random import randrange
from math import *

# TEMP GLOBAL VARIABLES
RADIUS = 18
DISTANCE = RADIUS * sqrt(3) 
ROWS = 14
COLUMNS_ODD = 7
COLUMNS_EVEN = 8
TOTAL_COLUMNS = COLUMNS_ODD + COLUMNS_EVEN
screenX,screenY = 640,480

class GameWorld:
    
    vX = 0 # Velocity of X direction.
    vY = 0 # Velocity of Y direction.
    
    bubblesOnBoard = [] # Bubbles in the game world. (fieldArray)
    connectedBubbles = [] # Bubbles of the same color & connected. (chainArray)
    attachedBubbles = [] # Bubbles attached to specific bubble. (connArray)
    
    timer = 0
    level = 0
    score = 0
    # maxLevel, highScore... lives?
    
    def init__level(self, level):
        self.level = level
        # BUILD LEVEL HERE (IMPLEMENT CURR DEFAULT).
        # bubblesOnBoard = []
    
class GameScreen:
    def __init__(self, gameWorld, screen):
        self.gameWorld = gameWorld
        print "TESTING"
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.backGroundLayer = pygame.Surface(screen.get_size())
        # DEFAULT: Level 1 Test
        bubblesOnBoard= [   [0,0,0,0,4,0,0,5],
                            [0,0,0,4,0,0,5],
                            [0,0,0,0,0,0,0,5],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0]]
        
        # Build right line border.
        self.borderLine()
        # Build cannon.
        self.buildCannon()

        self.loadBubbles(bubblesOnBoard)
        
    def borderLine(self):
        self.lineColor = (250,250,250)
        self.borderX = RADIUS+Bubble.radius * TOTAL_COLUMNS
        self.borderY = screenY
        pygame.draw.line(screen, self.lineColor, (self.borderX, 0), (self.borderX, screenY), 5)
        
    def buildCannon(self):
        self.cannonColor = (255,255,255)
        #Rectangle: Left,Top,Width, Height
        self.rectangle = [(RADIUS*8)-RADIUS, 450-RADIUS,2*RADIUS,2*RADIUS]
        self.startRadian = pi
        self.endRadian = 2*pi
        pygame.draw.arc(screen, self.cannonColor, self.rectangle, self.startRadian, self.endRadian,3)

        
    # Checks if a bubble should be placed
    def loadBubbles(self, bubblesOnBoard):
        self.bubblesOnBoard = bubblesOnBoard
        
        for row in range(ROWS):
            for col in range(COLUMNS_EVEN):
                # If it is an even row. Load 1st 7 rows with bubbles.
                if(row%2 == 0):
                    if(row < 8 and self.bubblesOnBoard[row][col] > 0):
                        self.placeBubble(row,col,bubblesOnBoard)

                    # If it's odd row: start grid slightly offset of left side of screen.
                else:
                    if(col < COLUMNS_ODD): # Implemented but not sure why???
                        if(row < 8 and self.bubblesOnBoard[row][col] > 0):
                            self.placeBubble(row,col,bubblesOnBoard)

    # Draws bubble on screen based on even or odd row.
    def placeBubble(self,x,y,bubblesOnBoard):
        self.row = x
        self.col = y
        if(x%2 == 0):
            x = RADIUS+self.col*RADIUS*2;
            # Y NEEDS TO BE AN INT?
            y = RADIUS+self.row*DISTANCE;
            bubble = Bubble(bubblesOnBoard[self.row][self.col], x, y)
            
            # TEMP CAST OF Y-COORD TO INTEGER
            pygame.draw.circle(screen, bubble.bubbleColor, (bubble.posX,int(bubble.posY)), RADIUS)
            GameWorld.connectedBubbles = []
            Bubble.checkBubbleChain(bubble, self.row,self.col,bubblesOnBoard)
# RECENT: ADDED GAMEWORLD.CONNECTED CLEAR.. SIZE IS STILL 1 -- CONTINUE TROUBLESHOOTING..
        else:
            x =  2*RADIUS+self.col*RADIUS*2
            y =  RADIUS+self.row*DISTANCE
            bubble = Bubble(bubblesOnBoard[self.row][self.col], x, y)
            pygame.draw.circle(screen, bubble.bubbleColor, (bubble.posX,int(bubble.posY)), RADIUS)
            GameWorld.connectedBubbles = []
            Bubble.checkBubbleChain(bubble,self.row,self.col,bubblesOnBoard)
        print GameWorld.connectedBubbles.__len__()
    


class Bubble:
    radius = RADIUS
    
    def __init__(self, bubbleColor, posX, posY):
        self.radius = RADIUS
        self.bubbleColor = self.pickColor(bubbleColor)
        self.posX = posX
        self.posY = posY

    def randomColor(self):
        bubbleCase = randrange(5)
        if(bubbleCase == 1):
            return (12,72,237)    # BLUE
        elif(bubbleCase == 2):
            return (237,12,34)    # RED
        elif(bubbleCase == 3):
            return (0,237,83)     # GREEN
        elif(bubbleCase == 4):
            return (224,255,51)   # YELLOW
        elif(bubbleCase == 5):
            return (255,255,255)  # WHITE
        
    def pickColor(self, number):
        bubbleCase = number
        if(bubbleCase == 1):
            return (12,72,237)    # BLUE
        elif(bubbleCase == 2):
            return (237,12,34)    # RED
        elif(bubbleCase == 3):
            return (0,237,83)     # GREEN
        elif(bubbleCase == 4):
            return (224,255,51)   # YELLOW
        elif(bubbleCase == 5):
            return (255,255,255)  # WHITE
        
    # Recursively create chain of matching bubbles that are attached.
    def checkBubbleChain(self, row,col, bubblesOnBoard):
        odd = row%2

        GameWorld.connectedBubbles.append(str(row)+","+str(col))
        i = -1
        j = -1
        while i <= 1:
            while j <= 1:
                if i != 0 or j != 0:
                    if i == 0 or j == 0 or (j==-1 and odd == 0) or (j==1 and odd ==1):
                        if self.inRange(row+i,col+j) and self.isNewChain(row+i, col+j,bubblesOnBoard[row][col], bubblesOnBoard):
                            self.checkBubbleChain(row+i, col+j,bubblesOnBoard)
                j+=1
            i+=1
    
    def inRange(self,x,y):
        if(x >= ROWS): return False
        if(y%2 == 0 and y >= COLUMNS_EVEN): return False
        if(y >= COLUMNS_ODD): return False
    
    def isNewChain(self,row, col, val, bubblesOnBoard):
        return val == self.getValue(row,col, bubblesOnBoard) and GameWorld.connectedBubbles.indexOf(row+","+col)==-1
        
    # SET ON GAMESCREEN NOT WORLD
    def getValue(self,row,col, bubblesOnBoard):
        print row
        print col
        if bubblesOnBoard[row] is None:
            return -1
        if bubblesOnBoard[row][col] is None:
            return -1
                
        return bubblesOnBoard[row][col]
    
# Initialize the game
pygame.init()

# Build screen
screen = pygame.display.set_mode((screenX, screenY),0,32)
clock = pygame.time.Clock()
gameWorld = GameWorld()
gameScreen = GameScreen(gameWorld, screen) # Class to build screen/play board.

gameRunning = True

while gameRunning:
    delta_Time = clock.tick(30) # 30 Frames per second?
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    
    pygame.display.update()


        
        