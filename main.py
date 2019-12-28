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



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Initializing the player

Player1 = Player("Gyxius", 1)
Player1.set_sprite('Sprites/002.png')
Player1.set_crop_image(Player1.image,(96,0,32,32))

# Initializing the NPC

NPC = {}
for i in range(ANIMALS_NUMBERS):
    NPC[i] = Animals("Animaux",i)
    NPC[i].set_sprite('Sprites/004.png')
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
            if event.key == pygame.K_SPACE:
                damaged_monsters_id = Player1.attack(Monsters,damaged_monsters_id)
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
            Player1.set_crop_image(Player1.image,(96,0,32,32))
    # Render the map
    screen.fill(WHITE)
    
    # Update and blit the player
    if Player1.life > 0:
        screen.blit(Player1.get_crop_image(),(Player1.getposx(),Player1.getposy()))
        Player1.draw_stats(screen)
    else:
        gameO = pygame.image.load("sprites/gameover.png")
        screen.blit(gameO,(0,0))

    pygame.display.update()

    




pygame.quit()
