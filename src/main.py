import pygame
from state import *
from settings import *
from game import Game
from stickman import *

def main():
    pygame.init()
    if pygame.joystick.get_count() > 0:
        pygame.joystick.Joystick(0).init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT),0,32)
    clock = pygame.time.Clock()

    g = Game()
    a = Attract()

    state = 0
    while 1:
        if state == 0:
            state = a.attract(screen,clock)
        if state == 1:
            state = g.tick(screen,clock)
        if state == 2:
            state = pause(screen,clock)
        if state == 3:
            state = game_over(screen,clock)
        if state == 4:
            exit()
        if state == 5:
            state = win(screen, clock)

if __name__ == '__main__': main()
