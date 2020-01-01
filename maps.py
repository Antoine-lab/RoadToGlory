import pygame
from random import *
from constants import *


class maps():
    """ Regroup all the setting of the map/grid """
    def __init__(self,col,row):
        self.f = 0
        self.g = 0
        self.h = 0
        self.col = col
        self.row = row
        self.posx = col*32
        self.posy = row*32
        self.count = 0
        self.neighbors = []
        self.image = pygame.image.load("sprites/test01.png")
        self.wall = False
        self.rock = False
        self.tree = False
        self.optimal = 0
        self.materials = randint(0,300)

        # Setting random walls(change value between 0 to 1)
        if(random()<0.1):
            self.wall=True
        if self.wall:
            if(random()<0.5):
                self.rock = True
            else:
                self.tree = True
                
    def draw(self,color):
       pygame.draw.rect(screen,(color),[WIDTH*self.col,HEIGHT*self.row,WIDTH,HEIGHT])
    
    def render(self,screen):
        land = (0,0,32,32)
        rock = (32,0,32,32)
        tree = (64,0,32,32)
        if self.wall:
            if self.rock:
                lol = self.image.subsurface(rock)
            else:
                lol = self.image.subsurface(tree)
        else:
            lol = self.image.subsurface(land)
            
        screen.blit(lol,(self.posx,self.posy))
        
        
    def addNeighbors(self,cell):
        i = self.col
        j = self.row
        if i < cols-1:
            self.neighbors.append(cell[i+1][j])
        if i > 0 :
            self.neighbors.append(cell[i-1][j])
        if j < rows-1:
            self.neighbors.append(cell[i][j+1])
        if j > 0:
            self.neighbors.append(cell[i][j-1])



def mapInit():
    
    #Initialise each cells
    for column in range(cols):
        grid.append([])
        for row in range(rows):
            grid[column].append(maps(column,row))

    # Adding neighbors
    for column in range(cols):
        for row in range(rows):
            grid[column][row].addNeighbors(grid)

    start = grid[0][rows-1]
    end = grid[cols-1][0]
    aStar(start,end)

def blockInit():
    blockList = []
    for column in range(cols):
        for row in range(rows):
            if (grid[column][row].wall)==True:
                x=int(WIDTH*grid[column][row].col)
                y=int(HEIGHT*grid[column][row].row)
                blockList.append(pygame.Rect((x,y,WIDTH,HEIGHT)))

    return blockList

def mapping(grid,screen):
    """ Render the map's sprites """
    screen.fill(WHITE)
    for column in range(cols):
        for row in range(rows):
            grid[column][row].render(screen)
            
def reSpawning(itemList):
    """ Respawn destroyed blocks """
    for item in itemList:
        item.count +=1
        if item.count == 30: # change this number to increase or decrease cooldown
            item.wall = True
            item.count = 0
            reSpawnList.remove(item)


def heuristics(a,b):
    """ Heuristics = distance between current position to the target's position """
    dist = abs(a.col-b.col)+ abs(a.row-b.row)
    return int(dist)

def aStar(start,end):
    """ aStar algorithm """
    #openSet is a list of node that need to be check in priority
    openSet = []
    #closedSet is a list of node that have been checked
    closedSet = []
    start.wall=False
    end.wall=False

    NICE = False
    openSet.append(start)
    #if openSet is not empty
    while len(openSet) > 0:

        # the best road is the one with the lowest f value
        best = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[best].f:
                best = i
        current = openSet[best]
        
        openSet.remove(current)
        neighbors = current.neighbors
        
        
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            # check if each neighbor is not inside closedSet and not a wall
            if (neighbor not in closedSet) and not(neighbor.wall):
                # g represent the distance between the current position and the starting position
                # +1 because each position moves by one cell at the time so the distance increase only by 1
                tempG = current.g+1
                if neighbor in openSet:
                    if tempG < neighbor.g:
                        neighbor.g = tempG
                else :
                    neighbor.g = tempG
                    openSet.append(neighbor)
                    
                neighbor.h = heuristics(neighbor,end)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.optimal = current
                
        closedSet.append(current)
            

        path = []
        temp = current
        path.append(temp)
        # as long as the current best position has a previous position
        # store the best path into path
        while(temp.optimal):
            path.append(temp.optimal)
            temp = temp.optimal

        # arrived to the target
        if current == end:
            NICE = True
            break
    #if no solution, load a new map
    if NICE == False:
        grid.clear()
        mapInit()
        print("Map not usable, resetting ...")

