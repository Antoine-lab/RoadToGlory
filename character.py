""" This file contains the superclass character and the subclasses monsters and players
"""
import pygame
from constants import *
import random


class Character(object):
    """ Basis for the players and all NPC characters """
    def __init__(self, id_character):
        """ Each character has a sprite and a unique id number """
        self.id = id_character
        self.life = 100
        self.position = 0 # it is the initial position of the sprite with 0 being bottom, 1 left, 2 right, and 3 top
        self.animation = 0
        
    def set_sprite(self,image):
        """ The method takes the link such as '002.png' and loads it """
        self.image = pygame.image.load(image)

    def set_crop_image(self,image,rect = (0,0,32,32)):
        """ the method takes a rectangle by default (0,128,32,32), gets the sprite in the form
        of a double list [x][y] and use the crop image """

        tempo2 = self.getsprite(rect)
        tempo = tempo2[self.position][self.animation]    # [0][0] is bottom, [1][0]is left etc.
        self.crop_image = self.image.subsurface(tempo)


    def get_crop_image(self):
        return self.crop_image
    
    def getposx(self):
        return self.posx
    
    def getposy(self):
        return self.posy

    def getsprite(self,rect00,size = 32):
        """ each sprite contains 8 characters, we just take one character and blit the approriate
        sprite according to the character movement """
        cropdown = (rect00,(rect00[0] + size,rect00[1],rect00[2],rect00[3]),(rect00[0] + 2*size,rect00[1],rect00[2],rect00[3]))
        cropleft = ((rect00[0],rect00[1] + size ,rect00[2],rect00[3]),(rect00[0] + size,rect00[1] + size ,rect00[2],rect00[3]),(rect00[0] + 2*size,rect00[1] + size,rect00[2],rect00[3]))
        cropright = ((rect00[0],rect00[1] + 2*size ,rect00[2],rect00[3]),(rect00[0] + size,rect00[1] + 2*size ,rect00[2],rect00[3]),(rect00[0] + 2*size,rect00[1] + 2*size,rect00[2],rect00[3]))
        cropup = ((rect00[0],rect00[1] + 3*size ,rect00[2],rect00[3]),(rect00[0] + size,rect00[1] + 3*size ,rect00[2],rect00[3]),(rect00[0] + 2*size,rect00[1] + 3*size,rect00[2],rect00[3]))
        crop = (cropdown,cropleft,cropright,cropup)
        return crop

    def get_rect(self):
        return pygame.Rect(self.posx,self.posy,32,32)
    def get_Frect(self):
        return pygame.Rect(self.Fx,self.Fy,32,32)
    
    def draw_stats(self, screen):
        pygame.draw.rect(screen,(0,128,0),[self.posx + 6,self.posy + 34,(self.life/4.5),3],0)
    
    def randomPos(self,grid):
        randomX = random.randint(0,SCREEN_WIDTH)//32
        randomY = random.randint(0,SCREEN_HEIGHT)//32
        while grid[randomX][randomY].wall == True:
            randomX = random.randint(0,SCREEN_WIDTH)//32
            randomY = random.randint(0,SCREEN_HEIGHT)//32
        return (randomX,randomY)
    
    
class Player(Character):
    """ The class contains all the methods and attributes for the player """
    def __init__(self, pseudo, id_character):
        Character.__init__(self, id_character)
        self.pseudo = pseudo
        self.posx = 0
        self.posy = int(rows*32)-32
        self.Fx = 0
        self.Fy = int(rows*32)-32
        self.stones = 0
        self.woods = 0
        
    def attack(self,monsters_dict,damaged_monsters_id):
        """ the method takes as input the monster dictionnary and check the position
        of each monster in order to attack the monster nearby """
        for key,value in monsters_dict.items():
            if self.position == 1: # 0 being bottom, 1 left, 2 right, and 3 top
                if ((self.posx // 32) - 1) == (value.posx // 32):
                    if (self.posy // 32) == (value.posy // 32):
                        damaged_monsters_id.append(key)
            if self.position == 0:
                if (self.posx // 32) == (value.posx // 32):
                    if ((self.posy // 32) + 1) == (value.posy // 32):
                        damaged_monsters_id.append(key)
            if self.position == 2:
                if (((self.posx + 32)// 32)) == (value.posx // 32):
                    if (self.posy // 32) == (value.posy // 32):
                        damaged_monsters_id.append(key)
            if self.position == 3:
                if (self.posx // 32) == (value.posx // 32):
                    if ((self.posy // 32) - 1) == (value.posy // 32):
                        damaged_monsters_id.append(key)
        return damaged_monsters_id
    
    def update(self,screen):
        if self.life > 0:
            screen.blit(self.get_crop_image(),(self.getposx(),self.getposy()))
            self.draw_stats(screen)
        else:
            gameO = pygame.image.load("sprites/gameover.png")
            screen.blit(gameO,(0,0))



class Animals(Character):
    """ The class contains all the methods and attributes for the monsters who doesn't move """
    def __init__(self, pseudo, id_character):
        Character.__init__(self, id_character)
        rand = self.randomPos(grid)
        self.posx = rand[0]*32
        self.posy = rand[1]*32
        self.pseudo = pseudo
        self.state = 'Neutral'
        self.damaged = False
        self.dead = False
    def get_state(self):
        return self.state
    def set_state(self,state):
        self.state = state

    def update(self,screen):
        if self.dead == False:
            screen.blit(self.get_crop_image(),(self.getposx(),self.getposy()))
            self.draw_stats(screen)
        if self.life <= 0:
            self.dead = True
            

            
        
       
class Monsters(Character):
    """ The class contains all the methods and attributes for the monsters who moves without the A* algorithm"""
    def __init__(self, pseudo, id_character):
        Character.__init__(self, id_character)
        self.pseudo = pseudo
        rand = self.randomPos(grid)
        self.posx = rand[0]*32
        self.posy = rand[1]*32
        self.state = 'Angry'
        self.damaged = False
        self.dead = False
    def get_state(self):
        return self.state
    def set_state(self,state):
        self.state = state
    def attack(self,player):
        if self.state == 'Angry':
            if abs(self.posx - player.posx) >32 :
                if self.posx - player.posx > 32 and  grid[int(self.posx/32)-1][int(self.posy/32)].wall != True and (SCREEN_WIDTH>self.posx>=0):
                    self.posx = self.posx - 32
                if player.posx - self.posx > 32 and grid[int(self.posx/32)+1][int(self.posy/32)].wall != True and (SCREEN_WIDTH>self.posx>=0):
                    self.posx = self.posx + 32
            if abs(self.posy - player.posy) >32:
                if self.posy - player.posy > 32 and  grid[int(self.posx/32)][int(self.posy/32)-1].wall != True and (SCREEN_HEIGHT>self.posy>=0):
                    self.posy = self.posy - 32
                if player.posy - self.posy > 32 and grid[int(self.posx/32)][int(self.posy/32)+1].wall != True and (SCREEN_HEIGHT>self.posy>=0):
                    self.posy = self.posy + 32
            if abs(self.posy - player.posy) <=32 and abs(self.posx - player.posx) <=32 and player.life > 0:
                player.life -= 5

    def update(self,screen):
        if self.dead == False:
            screen.blit(self.get_crop_image(),(self.getposx(),self.getposy()))
            self.draw_stats(screen)
