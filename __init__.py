'''
Created on May 30, 2014

@author: Alex Sullivan
'''


'''
NOTES UPDATED 6/25/2014
Alex's Notes
    - Been working on recognizing the chain. Made some good progress and as you can see based on the True's when you run the code there are some connections being made.
    - My work will continue to polish this backend chain identification. You will notice I added more methods to the Bubble class and completely got RID of the placeBubble method.
    - Hashs (#) that are all the way to the left represents Code that is commented out. I also denoted most of my comments with a Date (6/25/14) so you can see what I did.
    - Also note: The GameWorld class does not really do anything right now... It will be used once the graphics and mechanis are done and we can add levels, moving bubbles, etc.
    - Let me know if you have any questions
    - QUICK TEST FOR PULL REQUEST
Evan's Notes
    - 
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
    
    bubblesOnBoard = [[]] # Bubbles in the game world. (fieldArray)
    connectedBubbles = [[]] # Bubbles of the same color & connected. (chainArray)
    attachedBubbles = [[]] # Bubbles attached to specific bubble. (connArray)
    
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
                        bubble = Bubble(bubblesOnBoard[row][col], row, col)
#                         self.placeBubble(row,col,bubblesOnBoard,bubble)
                        pygame.draw.circle(screen, bubble.bubbleColor, (bubble.getPosX(row),int(bubble.getPosY(col))), RADIUS)
                        GameWorld.connectedBubbles = [] # Reset list to find new bubble chains. (6/25/14)
                        Bubble.checkBubbleChain(bubble, row, col,bubblesOnBoard)
                    
                    # If it's odd row: start grid slightly offset of left side of screen.
                else:
                    if(col < COLUMNS_ODD): # Implemented but not sure why???
                        if(row < 8 and self.bubblesOnBoard[row][col] > 0):
                            bubble = Bubble(bubblesOnBoard[row][col], row, col)
#                             self.placeBubble(row,col,bubblesOnBoard,bubble)
                            pygame.draw.circle(screen, bubble.bubbleColor, (bubble.getPosX(row),int(bubble.getPosY(col))), RADIUS)
                            GameWorld.connectedBubbles = [] # Reset list to find new bubble chains. (6/25/14)
                            Bubble.checkBubbleChain(bubble, row, col,bubblesOnBoard)

#         # Once all bubbles are loaded, Find connections. (6/25/14)
#         GameWorld.connectedBubbles = [] # Reset list to find new bubble chains. (6/25/14)
#         Bubble.checkBubbleChain(bubble, row, col,bubblesOnBoard)

#     # Draws bubble on screen based on even or odd row.
#     def placeBubble(self,x,y,bubblesOnBoard, bubble):
#         self.row = x
#         self.col = y
#         if(x%2 == 0):
#             x = RADIUS+self.col*RADIUS*2;
#             # Y is cast as an int for pygame
#             y = RADIUS+self.row*DISTANCE;
# #             GameWorld.connectedBubbles = [] # Reset list to find new bubble chains. (6/25/14) Moved check bubble up to the loadBubbles method for when everything finishes.
# #             Bubble.checkBubbleChain(bubble, self.row,self.col,bubblesOnBoard)
#             # Y is cast as an int for pygame
# 
# # RECENT: ADDED GAMEWORLD.CONNECTED CLEAR.. SIZE IS STILL 1 -- CONTINUE TROUBLESHOOTING..
#         else:
#             x =  2*RADIUS+self.col*RADIUS*2
#             y =  RADIUS+self.row*DISTANCE
# #             bubble = Bubble(bubblesOnBoard[self.row][self.col], x, y) #Moved up to loadBubble method
#             pygame.draw.circle(screen, bubble.bubbleColor, (bubble.posX,int(bubble.posY)), RADIUS)
# #             GameWorld.connectedBubbles = [] # Reset list to find new bubble chains. (6/25/14)
# #             Bubble.checkBubbleChain(bubble,self.row,self.col,bubblesOnBoard)
#         print GameWorld.connectedBubbles.__len__()
#     


class Bubble:
    radius = RADIUS
    
    def __init__(self, bubbleColor, row, col):
        self.radius = RADIUS
        self.bubbleColor = self.pickColor(bubbleColor)
        self.row = row
        self.col = col

        # Added position methods for the bubble class (6/25/2014)
    def getPosX(self, col):
        if( self.row%2 == 0):
            return RADIUS+self.col*RADIUS*2;
        else:
            return 2*RADIUS+self.col*RADIUS*2
            
    def getPosY(self, row):
        if( self.row%2 == 0):
            return RADIUS+self.row*DISTANCE;
        else:
            return RADIUS+self.row*DISTANCE       

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
                        print self.isNewChain(row+i,col+j,bubblesOnBoard[row][col], bubblesOnBoard)
                        if self.inRange(row+i,col+j) and self.isNewChain(row+i, col+j,bubblesOnBoard[row][col], bubblesOnBoard):
                            self.checkBubbleChain(row+i, col+j,bubblesOnBoard)
                j+=1
            i+=1
    
    # If the row and column exists return true. Else return false.
    def inRange(self,x,y):
        if(x >= ROWS): return False
        if(y%2 == 0 and y >= COLUMNS_EVEN): return False
        if(y >= COLUMNS_ODD): return False
        return True #ADDED 6/25/2014: May have been error (was returning none).
    
    def isNewChain(self,row, col, val, bubblesOnBoard):
        # Return if the value is equal to the x,y are equal to the bubblesOnBoard and connectedBubbles DOES NOT (6/25/14) contain the x,y.
#         print val
#         print self.getValue(row,col, bubblesOnBoard)
#         GameWorld.connectedBubbles.__contains__(str(row)+","+str(col))
        valuesMatch = val == self.getValue(row,col, bubblesOnBoard)
        if str(row)+","+str(col) in GameWorld.connectedBubbles:
            bubbleConnected = False
        else:
            bubbleConnected = True
        
        return bubbleConnected and valuesMatch
    
    # SET ON GAMESCREEN NOT WORLD
    def getValue(self,row,col, bubblesOnBoard):
        #Check Out of Range (6/25/2014) :: ADDED '-1' to account for index 0.
        if row > ROWS-1:
            return -1
        if col%2==0 and col > COLUMNS_EVEN-1:
            return -1
        if col > COLUMNS_ODD-1:
            return -1
        
        # Check if a bubble is on the board.
        """if bubblesOnBoard[row] is None: # Don't think this is needed (6/25/2014,amsully)
            return -1"""
        if bubblesOnBoard[row][col] == None:
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


        
        