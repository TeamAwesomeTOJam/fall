import pygame
from stickman import StickMan, Animation
import os
from settings import *


class SplashScreen(object):
    
    def __init__(self, default_animation):
        self.font_big = pygame.font.Font(os.path.join(RES, 'LiberationSans-Regular.ttf'), 60)
        self.font_small = pygame.font.Font(os.path.join(RES, 'LiberationSans-Regular.ttf'), 13)
        self.model = StickMan(os.path.join(RES, 'animations.pickle'))
        self.model.set_default_animation(default_animation)

class Attract(SplashScreen):

    def __init__(self):
        SplashScreen.__init__(self,1)

    def attract(self,screen,clock):
        time = clock.tick(60)/1000.0
        height = screen.get_height()
        width = screen.get_width()
        screen.fill((0,0,0))
 
        title = self.font_big.render('FALL', True, (255,255,255))
        screen.blit(title,((width - title.get_width())/2, (height - title.get_height())/2 - 100))
        
        credits = self.font_small.render('Created at TOJam by Jonathan Doda, Daniel Lister, and Michael Tao. With music and sounds by Troy Morrissey', True, (128,128,128))
        #credits2 = self.font_small.render('', True, (255,255,255))
        
        screen.blit(credits,((width - credits.get_width())/2, (height - credits.get_height()/2)-20))
        #screen.blit(credits2,((width - credits2.get_width())/2, (height - credits2.get_height())/2))
        
        self.model.update(time)
        surf = self.model.draw()
        screen.blit(surf, (width/2 + 50, height/2 + 50))
        
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                if e.key == pygame.K_RETURN:
                    return 1
            elif e.type == pygame.JOYBUTTONDOWN:
                if e.button == 1:
                    return 1
        pygame.display.flip()
        return 0

def pause(screen,clock):
    height = screen.get_height()
    width = screen.get_width()
    ingameSurface = screen.copy()
    ingameSurface.fill((255,255,255))
    rect=pygame.Surface((width,height),True,32)
    rect.fill((0,0,0))
    rect.set_alpha(40)
    ingameSurface.blit(rect,(0,0))
    #font = pygame.font.SysFont('helvetica',60)
    #font.set_bold(True)
    font_big = pygame.font.Font(os.path.join(RES, 'LiberationSans-Regular.ttf'), 60)
    pause=font_big.render('Paused',True,(255,0,0))
    screen.blit(pause,\
            ((width-pause.get_width())*.5,(height-pause.get_height())*.5))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                return 1
        elif e.type == pygame.JOYBUTTONDOWN:
            if e.button == 1:
                return 1
    clock.tick(10)
    screen.blit(ingameSurface,(0,0))
    pygame.display.flip()
    return 2

class GameOver(SplashScreen):
    
    def __init__(self):
        SplashScreen.__init__(self,8)

    def game_over(self, screen,clock):
        time = clock.tick(60)/1000.0
        height = screen.get_height()
        width = screen.get_width()
        screen.fill((0,0,0))
 
        title = self.font_big.render('Try Again', True, (255,0,0))
        screen.blit(title,((width - title.get_width())/2, (height - title.get_height())/2 - 100))
        self.model.update(time)
        surf = self.model.draw()
        screen.blit(surf, (width/2 + 50, height/2 + 50))
        
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                if e.key == pygame.K_RETURN:
                    return 1
                if e.key == pygame.K_ESCAPE:
                    return 0
            elif e.type == pygame.JOYBUTTONDOWN:
                if e.button == 1:
                    return 1
                if e.button == 2:
                    return 0
        pygame.display.flip()
        return 6


class Win(SplashScreen):

    def __init__(self):
        SplashScreen.__init__(self,7)
        
    def win(self,screen,clock):
        time = clock.tick(60)/1000.0
        height = screen.get_height()
        width = screen.get_width()
        screen.fill((0,0,0))
 
        title = self.font_big.render('You Win!', True, (80,80,255))
        screen.blit(title,((width - title.get_width())/2, (height - title.get_height())/2 - 100))
        self.model.update(time)
        surf = self.model.draw()
        screen.blit(surf, (width/2 + 50, height/2 + 50))
        
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                if e.key == pygame.K_RETURN:
                    return 5
            elif e.type == pygame.JOYBUTTONDOWN:
                if e.button == 1:
                    return 5
        pygame.display.flip()
        return 4
