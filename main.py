"""

@author: Mitsou, Antoine

Copyright (C) 2019,

"""
import pygame
from constants import *
from character import *
from maps import *

# Initializing pygame
pygame.init()
pygame.key.set_repeat(1,50)
mapInit()
block = blockInit()
clock = pygame.time.Clock()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Initializing the player

Player1 = Player("Gyxius", 1)
Player1.set_sprite('Sprites/002.png')
Player1.set_crop_image(Player1.image,(96,0,32,32))

# Initializing the NPC

NPC = {}
damaged_monsters_id = []
dead_monsters_id = set()

for i in range(ANIMALS_NUMBERS):
    NPC[i] = Animals("Animaux",i)
    NPC[i].set_sprite('Sprites/006.png')
    NPC[i].set_crop_image(NPC[i].image,(0,0,32,32))

for j in range(i+1,MONSTERS_NUMBERS + i + 1):
    NPC[j] = Monsters("Monstres",i)
    NPC[j].set_sprite('Sprites/004.png')
    NPC[j].set_crop_image(NPC[j].image,(96,0,32,32))

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:   
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                Player1.attack(NPC)
            elif keys[pygame.K_RIGHT]:
                Player1.position = 2
                Player1.Fx += move
                if (Player1.get_Frect().collidelist(block)) != -1 or Player1.Fx>(SCREEN_WIDTH-WIDTH):
                    Player1.Fx = Player1.posx
                else:
                    Player1.posx = Player1.Fx 
            elif keys[pygame.K_LEFT]:
                Player1.position = 1
                Player1.Fx -= move
                if (Player1.get_Frect().collidelist(block)) != -1 or Player1.Fx<0:
                    Player1.Fx = Player1.posx
                else:
                    Player1.posx = Player1.Fx 
            elif keys[pygame.K_UP]:
                Player1.position = 3
                Player1.Fy -= move
                if (Player1.get_Frect().collidelist(block)) != -1 or Player1.Fy<0:
                    Player1.Fy = Player1.posy
                else:
                    Player1.posy = Player1.Fy 
            elif keys[pygame.K_DOWN]:
                Player1.position = 0
                Player1.Fy += move
                if (Player1.get_Frect().collidelist(block)) != -1 or Player1.Fy>(SCREEN_HEIGHT-HEIGHT):
                    Player1.Fy = Player1.posy
                else:
                    Player1.posy = Player1.Fy
            
            #Putting blocks        
            elif keys[pygame.K_e]:
                X = Player1.posx//32
                Y = Player1.posy//32
                if Player1.position == 2:
                    grid[X+1][Y].wall = True
                if Player1.position == 1:
                    grid[X-1][Y].wall = True
                if Player1.position == 3:
                    grid[X][Y-1].wall = True
                if Player1.position == 0:
                    grid[X][Y+1].wall = True
                block = blockInit()
            #Remove blocks
            elif keys[pygame.K_r]:
                X = Player1.posx//32
                Y = Player1.posy//32
                if Player1.position == 2 and grid[X+1][Y].wall == True:
                    grid[X+1][Y].count +=1
                    if grid[X+1][Y].count == 5:
                        grid[X+1][Y].wall = False
                        grid[X+1][Y].count = 0
                        if grid[X+1][Y].rock:
                            Player1.stones += grid[X+1][Y].materials
                        else:
                            Player1.woods += grid[X+1][Y].materials
                        reSpawnList.append(grid[X+1][Y])
                        reSpawnList[-1].count = -5
                            
                if Player1.position == 1 and grid[X-1][Y].wall == True:
                    grid[X-1][Y].count +=1
                    if grid[X-1][Y].count == 5:
                        grid[X-1][Y].wall = False
                        grid[X-1][Y].count = 0
                        if grid[X-1][Y].rock:
                            Player1.stones += grid[X-1][Y].materials
                        else:
                            Player1.woods += grid[X-1][Y].materials
                        reSpawnList.append(grid[X-1][Y])
                        reSpawnList[-1].count = -5
                            
                if Player1.position == 3 and grid[X][Y-1].wall == True:
                    grid[X][Y-1].count +=1
                    if grid[X][Y-1].count == 5:
                        grid[X][Y-1].wall = False
                        grid[X][Y-1].count = 0
                        if grid[X][Y-1].rock:
                            Player1.stones += grid[X][Y-1].materials
                        else:
                            Player1.woods += grid[X][Y-1].materials
                        reSpawnList.append(grid[X][Y-1])
                        reSpawnList[-1].count = -5
                if Player1.position == 0 and grid[X][Y+1].wall == True:
                    grid[X][Y+1].count +=1
                    if grid[X][Y+1].count == 5:
                        grid[X][Y+1].wall = False
                        grid[X][Y+1].count = 0
                        if grid[X][Y+1].rock:
                            Player1.stones += grid[X][Y+1].materials
                        else:
                            Player1.woods += grid[X][Y+1].materials
                        reSpawnList.append(grid[X][Y+1])
                        reSpawnList[-1].count = -5
                
                
            elif keys[pygame.K_t]:
                print("Stones : ",Player1.stones)
                print("Woods : ",Player1.woods)
                
            
            
    # Render the map
##    screen.fill(WHITE)
    mapping(grid,screen)
    # ReSpawn destroyed blocks (method in maps.py)
    reSpawning(reSpawnList)
    block = blockInit()
    # Update the player
    Player1.animation = (Player1.animation + 1)%3
    Player1.set_crop_image(Player1.image,(96,0,32,32))
    Player1.update(screen)
    # Update the NPC
    
    for key,value in NPC.items():
        # Make the mobs move either toward the player if angry or randomly
        value.move(Player1)
        # blit and update the mobs
        value.update(screen)
        # Attack the player
        value.attack(Player1)
    pygame.display.update()
    clock.tick(10)
    




pygame.quit()
