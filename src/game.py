from settings import *
import os
import pygame
from pymunk import Vec2d
import pymunk as pm
from pygame.locals import *
from player import Player
import level
import gravityvolume
import math
import particles
from gravityvolume import GravityVolume
import portal
import coin


class Game(object):

    def __init__(self, level_path):
        self.game_over = False
        self.win = False
        self.camera_pos = Vec2d(0,0)
        
        self.on_screen = []
        self.particles = []
        self.shape_map = {}
        
        self.pan_left = False
        self.pan_right = False
        self.pan_up = False
        self.pan_down = False
        
        self.move_left = False
        self.move_right = False
        
        self.jump = False
        self.jump_time = 0
        
        self.swap_lr = False
        self.set_keys_later = False
        
        #Editor events
        self.mode_edit=False
        self.del_mode=False
        self.cmd_x=0
        self.cmd_y=0
        self.pos_start=None
        self.pos_end=None
        self.pos_mouse=None
        self.snap_radius=5.0
        self.dec_snap_radius=0
        self.inc_snap_radius=0
        
        #Load Sounds
        self.music = pygame.mixer.Sound(os.path.join(RES, 'music.ogg'))
        self.win_sound = pygame.mixer.Sound(os.path.join(RES, 'win.ogg'))
        self.win_sound.set_volume(0.6)
        self.lose_sound = pygame.mixer.Sound(os.path.join(RES, 'lose.ogg'))
        self.coin_sound = pygame.mixer.Sound(os.path.join(RES, 'coin.ogg'))
        
        self.music.play(-1)
        
        #PHYSICS!!!!
        pm.init_pymunk()
        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, 0.0)
        
        # Load level
        self.level_path = level_path
        try:
            self.level = level.load_level(self.level_path)
        except:
            self.level = level.Level()
        
        if not hasattr(self.level, 'coins'):
            self.level.coins = []

        for line in self.level.lines:
            self.shape_map[line.shape] = line
            self.space.add_static(line.shape)

        for gvol in self.level.gvols:
            self.shape_map[gvol.shape] = gvol
            self.space.add_static(gvol.shape)
        
        if self.level.goal:
            self.shape_map[self.level.goal.shape] = self.level.goal
            self.space.add_static(self.level.goal.shape)
            
        for cn in self.level.coins:
            self.shape_map[cn.shape] = cn
            self.space.add_static(cn.shape)

        #gravity polygons
        self.mode_gvol=False
        self.mode_grav_vec=False
        self.mode_grav_poly=False#check whether we've used this poly yet in list
        self.grav_set=False
        self.grav_vec=None
        self.poly_verts=[]
        
        #the player
        self.player = Player(self)
        self.space.add(self.player.body, self.player.shape)
        self.shape_map[self.player.shape] = self.player

        #the mouse
        self.mouse_body=pm.Body(pm.inf,pm.inf)
        mouse_shape=pm.Circle(self.mouse_body,3,Vec2d(0,0))
        mouse_shape.collision_type=COLLTYPE_MOUSE
        self.space.add(self.mouse_body,mouse_shape)
        
        self.space.add_collision_handler(COLLTYPE_DEFAULT, COLLTYPE_MOUSE, self.del_line,None,None,None)
        self.space.add_collision_handler(COLLTYPE_GRAVITY, COLLTYPE_MOUSE, self.del_gvol,None,None,None)
        self.space.add_collision_handler(COLLTYPE_LETHAL, COLLTYPE_MOUSE, self.del_line,None,None,None)
        self.space.add_collision_handler(COLLTYPE_COIN, COLLTYPE_MOUSE, self.del_coin,None,None,None)
                
        #The screen to collide with what we need to draw
        self.screen_body = pm.Body(pm.inf, pm.inf)
        self.screen_shape = None
        self.set_screen_shape()
        
        self.space.set_default_collision_handler(None, self.ignore_collision, None, None)
        self.space.add_collision_handler(COLLTYPE_DEFAULT, COLLTYPE_PLAYER, None, self.collect_player_collisions, None, None)
        self.space.add_collision_handler(COLLTYPE_GRAVITY, COLLTYPE_PLAYER, self.enter_gravity_volume, self.handle_gvol_collision, None, self.leave_gravity_volume)
        self.space.add_collision_handler(COLLTYPE_GRAVITY, COLLTYPE_PARTICLE, None, self.handle_gvol_collision, None, None)
        self.space.add_collision_handler(COLLTYPE_LETHAL, COLLTYPE_PLAYER, None, self.handle_lethal_collision, None, None)
        self.space.add_collision_handler(COLLTYPE_GOAL, COLLTYPE_PLAYER, None, self.handle_goal_collision, None, None)
        self.space.add_collision_handler(COLLTYPE_COIN, COLLTYPE_PLAYER, None, self.handle_coin_collision, None, None)
        
    def set_screen_shape(self):
        if self.screen_shape:
            self.space.remove(self.screen_shape)
        pts = map(self.screen2world,[(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)])
        self.screen_shape = pm.Poly(self.screen_body, pts)
        self.screen_shape.collision_type = COLLTYPE_SCREEN
        self.space.add(self.screen_shape)
        self.on_screen = []
    
    def ignore_collision(self, space, arbiter):
        s1, s2 = arbiter.shapes
        if s1 == self.screen_shape:
            self.on_screen.append(s2)
        elif s2 == self.screen_shape:
            self.on_screen.append(s1)
        return False
        
    def collect_player_collisions(self, space, arbiter):
        for c in arbiter.contacts:
            self.player.collisions.append(c.position)
        return True
    
    def handle_lethal_collision(self, space, arbiter):
        self.game_over = True
        return True
    
    def handle_goal_collision(self, space, arbiter):
        self.win = True
        return True
    
    def leave_gravity_volume(self, space, arbiter):
        self.set_keys_later = not self.on_ground()
        return True
    
    def enter_gravity_volume(self, space, arbiter):
        self.handle_gvol_collision(space, arbiter)
        if not self.on_ground():
            self.swap_keys()
        return True

    def handle_gvol_collision(self, space, arbiter):
        gvol_shape, shape = arbiter.shapes
        gvol = self.shape_map[gvol_shape]
        obj = self.shape_map[shape]
        obj.gravity_set = True
        body = shape.body
        body.reset_forces()
        body.apply_force((gvol.g[0] * body.mass, gvol.g[1] * body.mass))
        return False

    def handle_coin_collision(self, space, arbiter):
        player_shape, coin_shape = arbiter.shapes
        cn = self.shape_map[coin_shape]
        if cn.picked_up == False:
            self.coin_sound.play()
        cn.picked_up = True
        return False

    def del_line(self, space, arbiter):
        if self.del_mode:
            line_shape, mouse = arbiter.shapes
            line = self.shape_map[line_shape]
            self.level.dec_or_del(line.start)
            self.level.dec_or_del(line.end)
            del self.shape_map[line_shape]
            self.space.remove_static(line_shape)
            self.level.lines.remove(line)
        return False 

    def del_gvol(self, space, arbiter):
        if self.del_mode:
            gvol_shape, mouse = arbiter.shapes
            gvol = self.shape_map[gvol_shape]
            for m in gvol.vertices:
                self.level.dec_or_del(m)
            del self.shape_map[gvol_shape]
            self.space.remove_static(gvol_shape)
            self.level.gvols.remove(gvol)
        return False
    
    def del_coin(self, space, arbiter):
        if self.del_mode:
            coin_shape, mouse = arbiter.shapes
            cn = self.shape_map[coin_shape]
            del self.shape_map[coin_shape]
            self.space.remove_static(coin_shape)
            self.level.coins.remove(cn)
        return False

    def world2screen(self,v):
        x,y = v
        w = WIDTH
        h = HEIGHT
        rx = self.camera_pos.x
        ry = self.camera_pos.y
        return (int((x-rx)+w/2), int(-1*(y-ry)+h/2))
        
    def screen2world(self,v):
        x,y = v
        w = WIDTH
        h = HEIGHT
        rx = self.camera_pos.x
        ry = self.camera_pos.y
        return Vec2d((x-w/2) + rx,-1*(y-h/2)+ry)
    
    def on_ground(self):
        if self.player.last_on_ground > 0:
            return True
        for c in self.player.collisions:
            body_loc = self.player.body.world_to_local(c)
            #p = self.player.shape.body.position
            #a = (c - p).get_angle_degrees()
            #if abs(a + 90) < PLAYER_GROUND_COLLISION_ANGLE:
            if abs(body_loc.y - self.player.pts[0][1]) < 3:
                self.player.last_on_ground = DOWN_HILL_GRACE
                return True
        return False
    
    def swap_keys(self):
        if abs(Vec2d(0,-1).get_angle_between(self.player.body.force)) > math.pi/2.0:
            self.swap_lr = True
        else:
            self.swap_lr = False
        

    def handle_input(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
                
            elif e.type == pygame.KEYDOWN:
                if e.key == K_f:
                    pygame.display.toggle_fullscreen()
                if e.key == K_e:
                    self.mode_edit = not self.mode_edit
                elif self.mode_edit:
                    if e.key == K_a:
                        self.pan_left = True
                    elif e.key == K_d:
                        self.pan_right = True
                    elif e.key == K_w:
                        self.pan_up = True
                    elif e.key == K_s:
                        self.pan_down = True
                    elif e.key == K_COMMA :
                        self.dec_snap_radius= True
                    elif e.key == K_PERIOD :
                        self.inc_snap_radius = True
                    elif e.key == K_k :
                        self.level.save_level(self.level_path)
                    elif e.key == K_x :
                        self.del_mode=not self.del_mode
                    elif e.key == K_RETURN and self.mode_gvol:
                        self.mode_grav_vec = not self.mode_grav_vec
                        self.pos_start=None
                        self.pos_end=None
                    elif e.key == K_g :
                        if self.mode_gvol:#stopping gravity volume
                            self.grav_set=True
                        else: #starting gravity volume
                            self.mode_grav_vec=False
                            self.grav_set=False
                            self.poly_verts=[]
                            self.grav_vec=None
                        self.mode_gvol = not self.mode_gvol
                    elif e.key == K_m and self.del_mode and len(self.level.emitters)>0:
                        del self.level.emitters[-1]
                elif e.key == K_LEFT:
                    self.move_left = True
                    self.swap_keys()
                elif e.key == K_RIGHT:
                    self.move_right = True
                    self.swap_keys()
                elif e.key == K_SPACE and self.on_ground():
                    self.jump = True
                    self.jump_time = JUMP_TIME
                    self.player.jump()

            elif e.type == pygame.KEYUP:
                if self.mode_edit:
                    if e.key == K_a:
                        self.pan_left = False
                    elif e.key == K_d:
                        self.pan_right = False
                    elif e.key == K_w:
                        self.pan_up = False
                    elif e.key == K_s:
                        self.pan_down = False
                    elif e.key == K_COMMA :
                        self.dec_snap_radius= False 
                    elif e.key == K_PERIOD :
                        self.inc_snap_radius = False
                elif e.key == K_LEFT:
                    self.move_left = False
                elif e.key == K_RIGHT:
                    self.move_right = False
                elif e.key == K_SPACE:
                    self.jump = False
                    
            elif e.type == pygame.MOUSEBUTTONDOWN and self.mode_edit:
                if e.button == 1:
                    self.mode_grav_poly=True

                    pos_snap=self.level.check_snap(self.screen2world(e.pos),self.snap_radius)
                    if pos_snap is not None:
                        pos=pos_snap
                    else:
                        pos=self.screen2world(e.pos)
                    self.pos_start=pos
                
                elif e.button == 3:
                    pos = self.screen2world(e.pos)
                    self.level.emitters.append(particles.Emitter(pos))
                    
                elif e.button == 2:
                    pos = self.screen2world(e.pos)
                    if self.level.goal != None:
                        del self.shape_map[self.level.goal.shape]
                        self.space.remove_static(self.level.goal.shape)
                    self.level.goal = portal.Portal(pos)
                    self.shape_map[self.level.goal.shape] = self.level.goal
                    self.space.add_static(self.level.goal.shape)
                
                elif e.button == 4:
                    pos = self.screen2world(e.pos)
                    cn = coin.Coin(pos)
                    self.level.coins.append(cn)
                    self.shape_map[cn.shape] = cn
                    self.space.add_static(cn.shape)                          

            elif e.type == pygame.MOUSEBUTTONUP and self.mode_edit:
                if e.button == 1:
                    pos_snap=self.level.check_snap(self.screen2world(e.pos),self.snap_radius)
                    if pos_snap is not None:
                        pos=pos_snap
                    else:
                        pos=self.screen2world(e.pos)
                    self.pos_end=pos
                    
            elif e.type == JOYHATMOTION:
                x, y = e.value
                if x == 0:
                    self.move_left = False
                    self.move_right = False
                elif x == 1:
                    self.move_right = True
                    self.swap_keys()
                elif x == -1:
                    self.move_left = True
                    self.swap_keys()
            elif e.type == JOYAXISMOTION:
                if e.axis == 0:
                    if e.value < DEADZONE and e.value > -DEADZONE:
                        self.move_left = False
                        self.move_right = False
                    elif e.value >= DEADZONE:
                        self.move_right = True
                        self.swap_keys()
                    elif e.value <= -DEADZONE:
                        self.move_left = True
                        self.swap_keys()
            elif e.type == JOYBUTTONDOWN:
                if e.button == 1 and self.on_ground():
                    self.jump = True
                    self.jump_time = JUMP_TIME
                    self.player.jump()
                    
            elif e.type == JOYBUTTONUP:
                if e.button == 1:
                    self.jump = False

        if self.mode_edit:
            self.pos_mouse=pygame.mouse.get_pos()
            if self.pos_mouse is not None:
                self.pos_mouse=self.screen2world(self.pos_mouse)
                self.mouse_body.position=self.pos_mouse


    def tick(self,screen,clock):
        time = clock.tick(60)/1000.0
        #print 'fps: ' +  str(clock.get_fps())
        self.handle_input()

        if self.pan_left:
            self.camera_pos += Vec2d(-1 * PAN_SPEED, 0)
        if self.pan_right:
            self.camera_pos += Vec2d(PAN_SPEED, 0)
        if self.pan_up:
            self.camera_pos += Vec2d(0, PAN_SPEED)
        if self.pan_down:
            self.camera_pos += Vec2d(0, -1 * PAN_SPEED)
        
        #check to see if the player is allowed to move left/right
        allow_left = True
        allow_right = True
        #print 'collisions'
        for c in self.player.collisions:
            body_loc = self.player.body.world_to_local(c)
            #print body_loc
            #p = self.player.shape.body.position
            #a = (c - p).get_angle_degrees()
            #print a
            #if abs((a % 360) - 180) < PLAYER_WALL_COLLISION_ANGLE:
            if abs(body_loc.x - self.player.pts[1][0]) < 3:
                allow_left = False
            #if abs(a) < PLAYER_WALL_COLLISION_ANGLE:
            if abs(body_loc.x - self.player.pts[-2][0]) < 3:
                allow_right = False
            
        #control the player
        
        if not self.player.gravity_set:
            self.player.body.reset_forces()
            self.player.body.apply_force(Vec2d(0.0, -900 * self.player.body.mass))
        speed = 0
        if self.set_keys_later:
            self.swap_keys()
            self.set_keys_later = False
        elif abs(self.player.body.force.get_angle_between(self.player.last_gravity)) > math.pi/2:
            #print 'hello'
            self.swap_keys()
        
        #print self.player.body.force.get_angle_between(self.player.last_gravity)
        if self.swap_lr:
            m_left, m_right = self.move_right, self.move_left
        else:
            m_left, m_right = self.move_left, self.move_right
        if m_left and allow_left:
            speed -= PLAYER_SPEED
        if m_right and allow_right:
            speed += PLAYER_SPEED
        
        if self.jump and self.jump_time > 0:
            #print Vec2d(0,self.jump_time*JUMP_STRENGTH/JUMP_TIME).rotated(self.player.body.force.angle + math.pi/2)
            self.player.body.apply_impulse(Vec2d(0,self.jump_time*JUMP_STRENGTH/JUMP_TIME).rotated(self.player.body.force.angle + math.pi/2))
            self.jump_time -= time
        
        if self.player.last_on_ground > 0:
            self.player.last_on_ground -= time
        
        if speed and self.on_ground():
            self.player.walk()
        elif self.on_ground():
            self.player.idle()
        else:
            self.player.fly()
        
        #print Vec2d(self.player.body.force).rotated(-1*self.player.body.force.angle - math.pi/2).get_angle_degrees()
        #self.player.body.velocity = Vec2d(speed, self.player.body.velocity[1])
        v = Vec2d(self.player.body.velocity)
        v.rotate(-1*self.player.body.force.angle - math.pi/2)
        if self.on_ground():
            v.x = speed
        else:
            if speed > 0 and v.x < speed:
                v.x += AIR_CONTROL
            elif speed < 0 and v.x > speed:
                v.x -= AIR_CONTROL
        v.rotate(self.player.body.force.angle + math.pi/2)
        self.player.body.velocity = v
        #print v
        
        self.player.body.angle = self.player.body.force.rotated(math.pi/2.0).angle
        self.player.body.angular_velocity = 0
        
        if self.mode_edit:
            if self.dec_snap_radius:
                self.snap_radius-=1
                if self.snap_radius<1: self.snap_radius=1
            if self.inc_snap_radius:
                self.snap_radius+=1
            if self.mode_gvol:#doing gravity volume stuff
               
                #gravity vector mode, endpoints are defined
                if self.mode_grav_vec and self.pos_start is not None and self.pos_end is not None:
                    self.grav_vec =  (self.pos_end[0]-self.pos_start[0], self.pos_end[1]-self.pos_start[1])
                    self.pos_start=None
                    self.pos_end=None
                #not doing gravity vector
                elif self.mode_grav_vec is False and self.mode_grav_poly and self.pos_start is not None:
                    self.poly_verts.append((self.pos_start[0],self.pos_start[1]))
                    self.mode_grav_poly=False
                    

            elif self.pos_start is not None and self.pos_end is not None:
                body = pm.Body(pm.inf, pm.inf)
                shape = pm.Segment(body, self.pos_start, self.pos_end, 5.0)
                shape.friction = 1.0
                self.space.add_static(shape)
                if pygame.key.get_mods() & KMOD_SHIFT:
                    lethal = True
                else:
                    lethal = False
                line = level.Line(self.pos_start, self.pos_end, shape, lethal)
                self.level.add_line(line)
                self.shape_map[shape] = line
                self.pos_start = None
                self.pos_end = None
                
            #think gravity was set: add gravity object and clear our vars                
            if self.grav_set and self.mode_grav_vec is not None and self.poly_verts != []:
                gvol = GravityVolume(self.poly_verts, self.grav_vec)
                self.level.add_gvol(gvol)
                self.shape_map[gvol.shape] = gvol
                self.space.add_static(self.level.gvols[-1].shape)
                self.poly_verts = []
                self.grav_vec = None

        self.player.update(time)
        
        for e in self.level.emitters:
            e.update(self, time)
        
        dead_particles = []
        for i, p in enumerate(self.particles):
            if not p.gravity_set:
                p.body.reset_forces()
                p.body.apply_force(Vec2d(0.0, -900 * p.body.mass))
            p.ttl -= time
            if p.ttl < 0:
                dead_particles.append(i)
        for i in dead_particles:
            p = self.particles[i]
            self.space.remove(p.body, p.shape)
            del self.shape_map[p.shape]
            del self.particles[i]
                
        self.physics(time)
        
        if not self.player.was_on_ground and self.on_ground():
            self.player.was_on_ground = True
            self.player.land_sound.play()
            self.player.model.play_animation(4)
        elif not self.on_ground():
            self.player.was_on_ground = False 
        
        if self.player.last_gravity != self.player.body.force:
            self.player.gravity_sound.play()
        self.player.last_gravity = Vec2d(self.player.body.force)
        
        if not self.mode_edit:
            self.camera_pos = Vec2d(self.player.body.position)
        
        self.draw(screen)
        
        if self.game_over:
            self.music.stop()
            self.lose_sound.play()
            return 3
        elif self.win:
            self.music.stop()
            self.win_sound.play()
            return 4
        else:
            return 1
    
    def physics(self,time):
        self.set_screen_shape()
        self.player.collisions = []
        self.player.gravity_set = False
        for particle in self.particles:
            particle.gravity_set = False
        self.space.step(time)
    
    def draw(self,screen):
        screen.fill((0,0,0))

        # Draw start portal
        ox, oy = self.world2screen((0,0))
        pygame.draw.ellipse(screen, (255,237,3), pygame.Rect(ox - 30, oy - 60, 60, 120), 4)
        
        if self.mode_edit:
            pos_snap=self.level.check_snap(self.pos_mouse,self.snap_radius)
            if pos_snap is not None:
                pre_end=pos_snap
                pygame.draw.circle(screen, (255,0,0) , self.world2screen(pos_snap),int(self.snap_radius),1)
            else:
                pre_end=self.pos_mouse
            #Draw mouse drag
            if self.pos_start is not None and self.pos_mouse is not None:
                pygame.draw.line(screen, (255,255,255), self.world2screen(self.pos_start),self.world2screen(pre_end))
            #draw edit osd
            cmds = ["Save: k", "Pan Up: w", "Pan Left: a", "Pan Down: s", "Pan Right: d", "Toggle Edit mode: E",\
                    "Save: k", "Increase Snap Radius: .", "Decrease Snap Radius: ,", "Gravity Volume Mode: G", "Delete Mode: X"]
            if self.mode_gvol:
                cmds.append("Gravity Volume Mode ENABLED")
                if self.mode_grav_vec: cmds.append("Draw Gravity Vector: MOUSE1 drag")
                else: cmds.append("Draw Gravity Polygon: MOUSE1 click vertices")
            if self.del_mode:
                cmds.append("DELETE MODE: MOUSEOVER KILLS")
                cmds.append("Delete Last Emitter: m")
            font = pygame.font.SysFont('helvetica',14)
            for i in xrange(len(self.poly_verts)):
                pygame.draw.line(screen, (0,0,255), \
                        self.world2screen(self.poly_verts[i]),self.world2screen(self.poly_verts[(i+1)%len(self.poly_verts)]),10)

            for i in xrange(len(cmds)):
                cmd=cmds[i]
                surf=font.render(cmd,True,(80,80,80))
                screen.blit(surf,(self.cmd_x,self.cmd_y+i*surf.get_height()))

            points = self.player.shape.get_points()
            flipped = map(self.world2screen,points)
            pygame.draw.polygon(screen,(0,0,255),flipped,1)
            
            for e in self.level.emitters:
                e.draw(screen, self)

        #Draw other stuff
        for shape in self.on_screen:
            obj = self.shape_map.get(shape, None)
            if isinstance(obj, (level.Line, particles.Particle, Player, portal.Portal, coin.Coin)):
                obj.draw(screen, self)
            elif isinstance(obj, GravityVolume) and self.mode_edit:
                obj.draw(screen, self)

        pygame.display.flip()
        
