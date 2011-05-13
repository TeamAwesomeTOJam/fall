import math

import pygame
from pygame.locals import *


class StickMan(object):

    def __init__(self):
        self.surface = pygame.Surface((128, 128))
        self.upper_arm_length = 40
        self.lower_arm_length = 40
        self.upper_leg_length = 40
        self.lower_leg_length = 40
        self.head_radius = 20
        self.torso_length = 40
        self.hip_to_shoulders = 30
        self.animations = self.load_animations()
        self.animation = None
        self.prev_frame = None
        self.next_frame = None
        self.frame_index = 0
        self.frame_duration = 1
        self.frame_elapsed = 0
        
    def _get_endpoint(self, start, angle, length):
        x = start[0] + length * math.cos(angle)
        y = start[1] + length * math.sin(angle)
        return (x, y)
        
    def load_animations(self):
        pass
    
    def save_animations(self):
        pass

    def update(self, delta):
        self.frame_elapsed += delta
        if self.frame_elapsed >= self.frame_duration:
            self.frame_elapsed = 0
            self.prev_frame = self.next_frame
            self.frame_index += 1
            if self.frame_index >= len(self.animation):
                self.frame_index = 0
            self.next_frame = self.animation[self.frame_index]
    
    def draw(self):
        pass

class Animation(object):
    
    def __init__(self, duration, frames):
        self.duration = duration
        self.frames = frames
    
    def __index__(self, idx):
        return self.frames[idx]
    
    def __iter__(self):
        return self.frames.__iter__
        
    @property
    def frame_duration(self):
        return self.duration / len(self.frames)
    

class AnimationFrame(object):
    
    def __init__(self, l_shoulder, r_shoulder, l_elbow, r_elbow, l_hip, r_hip, l_knee, r_knee, lean):
        self.l_shoulder = l_shoulder
        self.r_shoulder = r_shoulder
        self.l_elbow = l_elbow
        self.r_elbow = r_elbow
        self.l_hip = l_hip
        self.r_hip = r_hip
        self.l_knee = l_knee
        self.r_knee = r_knee
        self.lean = lean