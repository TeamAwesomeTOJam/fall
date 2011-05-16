import sys
import os.path

ROOT = os.path.normpath(os.path.join(sys.path[0], '..')) 
RES = os.path.join(ROOT, 'res')


LEVELS = ['level.daniel.0.pickle', 
          'level.jon.1.pickle', 
          'level.tao.0.pickle', 
          'level.daniel.1.pickle', 
          'level.jon.2.pickle', 
          'level.daniel.2.pickle', 
          'level.daniel.3.pickle',
          'level.jon.3.pickle',
          'level.jon.4.pickle',
          'level.daniel.4.pickle',
          'level.tao.1.pickle',
          'level.tao.2.pickle']

WIDTH = 800
HEIGHT = 600

PAN_SPEED = 5


#PYMUNK COLLISION TYPES

COLLTYPE_DEFAULT = 0
COLLTYPE_SCREEN = 1
COLLTYPE_PLAYER = 2
COLLTYPE_GRAVITY = 3
COLLTYPE_LETHAL = 4
COLLTYPE_GOAL = 5
COLLTYPE_PARTICLE = 6
COLLTYPE_MOUSE = 7
COLLTYPE_COIN = 8

#Player physics

PLAYER_MASS = 10
PLAYER_RADIUS = 20
PLAYER_FRICTION = 1.0

PLAYER_SPEED = 200

PLAYER_WALL_COLLISION_ANGLE = 30
PLAYER_GROUND_COLLISION_ANGLE = 50

JUMP_TIME = 0.3
JUMP_STRENGTH = 700

DEADZONE = 0.3

DOWN_HILL_GRACE = 0.2
FLIP_THRESHOLD = 50

AIR_CONTROL = 10

EMITTER_PERIOD = 0.05
