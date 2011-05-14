import pygame
from state import *

class game:
	def __init__(self):
		pygame.init()
		screen = pygame.display.set_mode((640,400),0,32)
		clock = pygame.time.Clock()


		state=0
		while 1:
			if state == 0:
				state = attract(screen,clock)
			if state == 1:
				state = play_game(screen,clock)
			if state == 2:
				state = pause(screen,clock)
			if state == 3:
				state = game_over(screen,clock)
			if state == 4:
				exit()
			state = 0


	



def main():
	game()

if __name__ == '__main__': main()
