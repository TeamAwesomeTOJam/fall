import os, sys
import math
import pickle

import pygame
from pygame.locals import *

import settings

SPINE = 0
L_SHOULDER = 1
R_SHOULDER = 2
L_ELBOW = 3
R_ELBOW = 4
L_HIP = 5
R_HIP = 6
L_KNEE = 7
R_KNEE = 8
Y_OFFSET = 9
DURATION = 10


class StickMan(object):

    def __init__(self, animation_path):
        self.color = (255, 255, 255)
        self.width = 2
        self.upper_arm_length = 18
        self.lower_arm_length = 18
        self.upper_leg_length = 24
        self.lower_leg_length = 24
        self.head_radius = 16
        self.torso_length = 32
        self.animation_path = animation_path
        self.animations = self.load_animations()
        self.animation = self.animations[0]
        self.default_animation = self.animations[0]
        self.prev_frame = self.animation[0]
        self.next_frame = self.animation[0]
        self.frame_index = 0
        self.frame_elapsed = 0
        
    def _get_endpoint(self, start, angle, length):
        x = int(start[0] + length * math.cos(angle))
        y = int(start[1] + length * math.sin(angle))
        return (x, y)
        
    def load_animations(self):
        try:
            in_file = open(self.animation_path, 'rb')
            animations = pickle.load(in_file)
            for animation in animations:
                animation.repeat = False
                for frame in animation:
                    if len(frame) == 9:
                        frame.append(48.0)
            return animations
        except IOError:
            return [Animation()]
    
    def save_animations(self):
        out_file = open(self.animation_path, 'wb')
        pickle.dump(self.animations, out_file)

    def play_animation(self, idx, repeat=False):
        if isinstance(idx, Animation):
            self.animation = idx
        else:
            self.animation = self.animations[idx]
        self.animation.repeat = repeat
        self.frame_index = 0
        self.prev_frame = self.next_frame
        self.next_frame = self.animation[self.frame_index]
        
    def set_default_animation(self, idx):
        old_default = self.default_animation
        self.default_animation = self.animations[idx]
        if self.animation == old_default and old_default != self.default_animation:
            self.play_animation(idx, repeat=True)
        
    def show_frame(self, idx):
        self.frame_index = idx
        self.frame_elapsed = 0
        self.prev_frame = self.animation[self.frame_index]
        self.next_frame = self.animation[(self.frame_index + 1) % len(self.animation)]

    def update(self, dt):
        self.frame_elapsed += dt
        if self.frame_elapsed >= self.animation.frame_duration:
            self.frame_elapsed -= self.animation.frame_duration
            self.prev_frame = self.next_frame
            self.frame_index = (self.frame_index + 1) % len(self.animation)
            if self.frame_index == 0:
                if self.animation.repeat:
                    self.next_frame = self.animation[self.frame_index]
                else: 
                    self.play_animation(self.default_animation, repeat=True)
            else:
                self.next_frame = self.animation[self.frame_index]
    
    def draw(self, editor=False, selection=None):
        ratio = self.frame_elapsed / self.animation.frame_duration
        i_frame = [pf * (1 - ratio) + nf * (ratio) for pf, nf in zip(self.prev_frame, self.next_frame)]
        
        hip_pos = (64, i_frame[Y_OFFSET])
        shoulder_pos = self._get_endpoint(hip_pos, i_frame[SPINE], self.torso_length * 0.9)
        neck_pos = self._get_endpoint(hip_pos, i_frame[SPINE], self.torso_length)
        head_pos = self._get_endpoint(hip_pos, i_frame[SPINE], self.torso_length + self.head_radius)
        l_elbow_pos = self._get_endpoint(shoulder_pos, i_frame[SPINE] + i_frame[L_SHOULDER], self.upper_arm_length) 
        r_elbow_pos = self._get_endpoint(shoulder_pos, i_frame[SPINE] + i_frame[R_SHOULDER], self.upper_arm_length)
        l_hand_pos = self._get_endpoint(l_elbow_pos, i_frame[SPINE] + i_frame[L_SHOULDER] + i_frame[L_ELBOW], self.lower_arm_length)
        r_hand_pos = self._get_endpoint(r_elbow_pos, i_frame[SPINE] + i_frame[R_SHOULDER] + i_frame[R_ELBOW], self.lower_arm_length)
        l_knee_pos = self._get_endpoint(hip_pos, i_frame[L_HIP], self.upper_leg_length)
        r_knee_pos = self._get_endpoint(hip_pos, i_frame[R_HIP], self.upper_leg_length)
        l_foot_pos = self._get_endpoint(l_knee_pos, i_frame[L_HIP] + i_frame[L_KNEE], self.lower_leg_length)
        r_foot_pos = self._get_endpoint(r_knee_pos, i_frame[R_HIP] + i_frame[R_KNEE], self.lower_leg_length)
        
        surface = pygame.Surface((128, 128), flags=SRCALPHA)
        surface.fill((0,0,0,0))
        lines = [(hip_pos, neck_pos),
                 (shoulder_pos, l_elbow_pos),
                 (shoulder_pos, r_elbow_pos),
                 (l_elbow_pos, l_hand_pos),
                 (r_elbow_pos, r_hand_pos),
                 (hip_pos, l_knee_pos),
                 (hip_pos, r_knee_pos),
                 (l_knee_pos, l_foot_pos),
                 (r_knee_pos, r_foot_pos)]
        for i, (start, end) in enumerate(lines):
            if editor:
                if i == selection:
                    pygame.draw.line(surface, (255,255,0), start, end, self.width)
                elif i == 0:
                    pygame.draw.line(surface, self.color, start, end, self.width)
                elif i % 2: # odd limb, left side
                    pygame.draw.line(surface, (0,255,0), start, end, self.width)
                else: # even limb, right side
                    pygame.draw.line(surface, (255,0,0), start, end, self.width)   
            else:
                pygame.draw.line(surface, self.color, start, end, self.width)
        pygame.draw.circle(surface, self.color, head_pos, self.head_radius, self.width)

        return surface
        

class Animation(object):
    
    def __init__(self, duration=1.0, frames=None):
        self.duration = duration
        if frames:
            self.frames = frames
        else:
            self.frames = [[-math.pi*0.5, -math.pi*0.5, math.pi*0.5, 1, -1,  -math.pi * 1.25, -math.pi * 1.75, 0, 0, 80]]
        self.repeat = False
    
    def __len__(self):
        return len(self.frames)
    
    def __getitem__(self, idx):
        return self.frames[idx]
    
    def __setitem(self, idx, value):
        self.frames[idx] = value
        
    def __delitem(self, idx):
        del self.frames[idx]
    
    def __iter__(self):
        return self.frames.__iter__()
        
    @property
    def frame_duration(self):
        return self.duration / len(self.frames)
    

if __name__ == '__main__':
    pygame.init()
    pygame.key.set_repeat(500, 100)
    screen = pygame.display.set_mode((256, 128))
    font = pygame.font.Font(None, 24)
    sm = StickMan(os.path.join(settings.RES, 'animations.pickle'))
    control = 0
    frame = 0
    animation = 0
    play = False
    clock = pygame.time.Clock()
    
    while True:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_s:
                sm.save_animations()
            elif event.type == KEYDOWN and event.key == K_n:
                sm.animations.append(Animation())
            elif event.type == KEYDOWN and event.key == K_p:
                play = not play
            elif event.type == KEYDOWN and event.key == K_BACKQUOTE:
                del sm.animation.frames[sm.frame_index]
                sm.frame_index = sm.frame_index % len(sm.animation)
                sm.show_frame(sm.frame_index)
            elif event.type == KEYDOWN and event.key == K_LEFTBRACKET:
                control = (control - 1) % (len(sm.prev_frame) + 1)
            elif event.type == KEYDOWN and event.key == K_RIGHTBRACKET:
                control = (control + 1) % (len(sm.prev_frame) + 1)
            elif event.type == KEYDOWN and event.key == K_EQUALS:
                if control == DURATION:
                    sm.animation.duration += 0.1
                elif control == Y_OFFSET:
                    sm.prev_frame[control] += 1
                else:
                    sm.prev_frame[control] += 0.1
            elif event.type == KEYDOWN and event.key == K_MINUS:
                if control == DURATION:
                    sm.animation.duration -= 0.1
                elif control == Y_OFFSET:
                    sm.prev_frame[control] -= 1
                else:
                    sm.prev_frame[control] -= 0.1
            elif event.type == KEYDOWN and event.key == K_LEFT:
                frame = (frame - 1) % len(sm.animation)
                sm.show_frame(frame)
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                frame = (frame + 1) % len(sm.animation)
                sm.show_frame(frame)
            elif event.type == KEYDOWN and event.key == K_UP:
                animation = (animation - 1) % len(sm.animations)
                sm.play_animation(animation, repeat=True)
                sm.show_frame(0)
            elif event.type == KEYDOWN and event.key == K_DOWN:
                animation = (animation + 1) % len(sm.animations)
                sm.play_animation(animation, repeat=True)
                sm.show_frame(0)
            elif event.type == KEYDOWN and event.key == K_COMMA:
                new_frame = list(sm.prev_frame)
                sm.animation.frames.insert(sm.frame_index, new_frame)
                sm.show_frame(sm.frame_index)
            elif event.type == KEYDOWN and event.key == K_PERIOD:
                new_frame = list(sm.prev_frame)
                if sm.frame_index + 1 == len(sm.animation):
                    sm.animation.frames.append(new_frame)
                else:
                    sm.animation.frames.insert(sm.frame_index + 1, new_frame)
                sm.show_frame(sm.frame_index + 1)
                        
        if play:
            sm.update(dt)
        
        screen.fill((0,0,0,255))
        surf = sm.draw(editor=True, selection=control)
        screen.blit(surf, (0,0))
        screen.blit(font.render('Frame %s/%s' % (sm.frame_index+1, len(sm.animation)), True, (255,255,255)), (128, 0))
        screen.blit(font.render('Animation %s/%s' % (animation+1, len(sm.animations)), True, (255,255,255)), (128, 24))
        if control == Y_OFFSET:
            screen.blit(font.render('Y Offset %.2f' % (sm.prev_frame[Y_OFFSET],), True, (255,255,0)), (128, 48))
        elif control == DURATION:
            screen.blit(font.render('Duration %.2f' % (sm.animation.duration,), True, (255,255,0)), (128, 48))
        else:
            screen.blit(font.render('Angle %.2f' % (sm.prev_frame[control],), True, (255,255,0)), (128, 48))
        pygame.display.flip()

