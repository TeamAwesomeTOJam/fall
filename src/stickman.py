import math

import pygame
from pygame.locals import *

SPINE = 0
L_SHOULDER = 1
R_SHOULDER = 2
L_ELBOW = 3
R_ELBOW = 4
L_HIP = 5
R_HIP = 6
L_KNEE = 7
R_KNEE = 8


class StickMan(object):

    def __init__(self):
        self.color = (255, 255, 255, 255)
        self.width = 2
        self.upper_arm_length = 18
        self.lower_arm_length = 18
        self.upper_leg_length = 24
        self.lower_leg_length = 24
        self.head_radius = 16
        self.torso_length = 32
        self.animations = self.load_animations()
        self.animation = self.animations['idle']
        self.prev_frame = self.animation[0]
        self.next_frame = self.animation[0]
        self.frame_index = 0
        self.frame_elapsed = 0
        
    def _get_endpoint(self, start, angle, length):
        x = int(start[0] + length * math.cos(angle))
        y = int(start[1] + length * math.sin(angle))
        return (x, y)
        
    def load_animations(self):
        return {'idle' : Animation(1.0, [[-math.pi*0.5, -math.pi*0.5, math.pi*0.5, 1, -1,  -math.pi * 1.25, -math.pi * 1.75, 0, 0]])}
    
    def save_animations(self):
        pass

    def update(self, delta):
        self.frame_elapsed += delta
        if self.frame_elapsed >= self.animation.frame_duration:
            self.frame_elapsed -= self.animation.frame_duration
            self.prev_frame = self.next_frame
            self.frame_index = (self.frame_index + 1) % len(self.animation)
            self.next_frame = self.animation[self.frame_index]
    
    def draw(self, selection=None):
        ratio = self.frame_elapsed / self.animation.frame_duration
        i_frame = [pf * (1 - ratio) + nf * (ratio) for pf, nf in zip(self.next_frame, self.prev_frame)]
        
        hip_pos = (64, 64)
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
            if i == selection:
                pygame.draw.line(surface, (255,255,0), start, end, self.width)
            else:
                pygame.draw.line(surface, self.color, start, end, self.width)
        pygame.draw.circle(surface, self.color, head_pos, self.head_radius, self.width)

        return surface
        

class Animation(object):
    
    def __init__(self, duration, frames):
        self.duration = duration
        self.frames = frames
    
    def __getitem__(self, idx):
        return self.frames[idx]
    
    def __iter__(self):
        return self.frames.__iter__
        
    @property
    def frame_duration(self):
        return self.duration / len(self.frames)
    

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((128, 128))
    font = pygame.font.Font(None, 24)
    sm = StickMan()
    joint = 0
    
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_UP:
                joint = (joint + 1) % 9
            elif event.type == KEYDOWN and event.key == K_DOWN:
                joint = (joint - 1) % 9
            elif event.type == KEYDOWN and event.key == K_EQUALS:
                sm.prev_frame[joint] += 0.1
            elif event.type == KEYDOWN and event.key == K_MINUS:
                sm.prev_frame[joint] -= 0.1
        
        screen.fill((0,0,0,255))
        surf = sm.draw(selection=joint)
        screen.blit(surf, (0,0))
        text = font.render(str(joint), True, (255,255,255))
        screen.blit(text, (100, 100)) 
        pygame.display.flip()

