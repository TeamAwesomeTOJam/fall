import pygame
from stickman import StickMan, Animation
import os
from settings import *



class Attract(object):

    def __init__(self):
        self.model = StickMan(os.path.join(RES, 'animations.pickle'))
        self.model.set_default_animation(1)
        self.font_big = pygame.font.Font(os.path.join(RES, 'LiberationSans-Regular.ttf'), 60)

    def attract(self,screen,clock):
        time = clock.tick(60)/1000.0
        height = screen.get_height()
        width = screen.get_width()
        screen.fill((0,0,0))
        #font = pygame.font.SysFont('helvetica',60)
        #font.set_bold(True)
        #press=font.render('Press',True,(255,0,0))
        #start=font.render('ENTER',True,(255,0,0))
        #screen.blit(press,\
        #        ((width-press.get_width())*.5,height*.5-press.get_height()))
        #screen.blit(start,\
        #        ((width-start.get_width())*.5,height*.5))
        
        title = self.font_big.render('FALL', True, (255,255,255))
        screen.blit(title,((width - title.get_width())/2, (height - title.get_height())/2 - 100))
        self.model.update(time)
        surf = self.model.draw()
        screen.blit(surf, (width/2 + 50, height/2 + 50))
        
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return 1
        pygame.display.flip()
        return 0


def play_game(screen,clock):
    return 3

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
    clock.tick(10)
    screen.blit(ingameSurface,(0,0))
    pygame.display.flip()
    return 2

def game_over(screen,clock):
    height = screen.get_height()
    width = screen.get_width()
    screen.fill((0,0,0))
    #font = pygame.font.SysFont('helvetica',60)
    #font.set_bold(True)
    font_big = pygame.font.Font(os.path.join(RES, 'LiberationSans-Regular.ttf'), 60)
    gameover=font_big.render('Game Over',True,(255,0,0))
    screen.blit(gameover,\
            ((width-gameover.get_width())*.5,(height-gameover.get_height())*.5))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                return 0
            if e.key == pygame.K_RETURN:
                return 1
    clock.tick(10)
    pygame.display.flip()
    return 3

def win(screen,clock):
    height = screen.get_height()
    width = screen.get_width()
    screen.fill((0,0,0))
    #font = pygame.font.SysFont('helvetica',60)
    #font.set_bold(True)
    font_big = pygame.font.Font(os.path.join(RES, 'LiberationSans-Regular.ttf'), 60)
    gameover=font_big.render('You Win!',True,(80,80,255))
    screen.blit(gameover,\
            ((width-gameover.get_width())*.5,(height-gameover.get_height())*.5))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                return 0
    clock.tick(10)
    pygame.display.flip()
    return 5
