import pygame

def attract(screen,clock):
	height = screen.get_height()
	width = screen.get_width()
	screen.fill((150,150,150))
	font = pygame.font.SysFont('helvetica',60)
	font.set_bold(True)
	press=font.render('Press',True,(255,0,0))
	start=font.render('ENTER',True,(255,0,0))
	screen.blit(press,\
			((width-press.get_width())*.5,height*.5-press.get_height()))
	screen.blit(start,\
			((width-start.get_width())*.5,height*.5))
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			exit()
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_RETURN:
				return 1
	clock.tick(10)
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
	font = pygame.font.SysFont('helvetica',60)
	font.set_bold(True)
	pause=font.render('Paused',True,(255,0,0))
	screen.blit(pause,\
			((width-pause.get_width())*.5,(height-pause.get_height())*.5))
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			exit()
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_RETURN:
				return 1
	clock.tick(10)
	pygame.blit(ingameSurface,(0,0))
	pygame.display.flip()
	return 2

def game_over(screen,clock):
	height = screen.get_height()
	width = screen.get_width()
	screen.fill((150,150,150))
	font = pygame.font.SysFont('helvetica',60)
	font.set_bold(True)
	gameover=font.render('Game Over',True,(255,0,0))
	screen.blit(gameover,\
			((width-gameover.get_width())*.5,(height-gameover.get_height())*.5))

	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			exit()
		if e.type == pygame.KEYDOWN:
			if e.key == pygame.K_RETURN:
				return 4
	clock.tick(10)
	pygame.display.flip()
