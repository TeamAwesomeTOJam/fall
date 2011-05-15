import pygame
from state import *
from settings import *
from game import Game
from stickman import *

def main():
    pygame.init()
    if pygame.joystick.get_count() > 0:
        pygame.joystick.Joystick(0).init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()

    a = Attract()

    state = 5
    while 1:
        if state == 0:
            state = a.attract(screen,clock)
        if state == 1:
            state = game.tick(screen,clock)
            if state == 4:
                level_idx += 1
                if level_idx < len(LEVELS):
                    game = Game(os.path.join(RES, LEVELS[level_idx]))
                    state = 1
        if state == 2:
            state = pause(screen,clock)
        if state == 3:
            state = game_over(screen,clock)
            if state == 1:
                game = Game(os.path.join(RES, LEVELS[level_idx]))
        if state == 4:
            state = win(screen, clock)
        if state == 5:
            level_idx = 0
            game = Game(os.path.join(RES, LEVELS[level_idx]))
            state = 0
            

if __name__ == '__main__': 
    main()
