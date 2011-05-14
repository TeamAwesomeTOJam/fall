import sys
import os.path

ROOT = os.path.normpath(os.path.join(sys.path[0], '..')) 
RES = os.path.join(ROOT, 'res')

WIDTH = 800
HEIGHT = 600

PAN_SPEED = 5


#PYMUNK COLLISION TYPES

COLLTYPE_DEFAULT = 0
COLLTYPE_SCREEN = 1
COLLTYPE_PLAYER = 2

#Player physics

PLAYER_MASS = 10
PLAYER_RADIUS = 10
PLAYER_FRICTION = 1.0
