import pygame
from random import randint, uniform
import math
from pygame.math import Vector2 as vector2
from config import *


class HeartEmmitterParticle(object):
    def __init__(self, x, y, firework, colour, i, angle, stable_size):
        self.stay_shape = False
        self.angle = angle
        
        self.firework = firework
        self.pos = vector2(x, y)
        self.origin = vector2(x, y)
        self.acc = vector2(0, 0)
        self.remove = False
        self.explosion_radius = randint(EXPLOSION_RADIUS_MIN, EXPLOSION_RADIUS_MAX)
        self.life = 0
        self.colour = colour
        self.t = i
        self.vel = vector2(16*math.sin(self.t)**3, 13*math.cos(self.t) - 5*math.cos(2*self.t) - 2*math.cos(3*self.t) - math.cos(4*self.t))
        self.stable_size = stable_size
        self.size = randint(PARTICLE_SIZE - 1, PARTICLE_SIZE + 1)
        self.move()
        self.outside_spawn_radius()

    def update(self) -> None:
        # called every frame
        self.life += 1
        self.move()
        self.vel = vector2(16*math.sin(self.t)**3, 13*math.cos(self.t) - 5*math.cos(2*self.t) - 2*math.cos(3*self.t) - math.cos(4*self.t))
        self.apply_force(vector2(uniform(-1, 1) / X_WIGGLE_SCALE, GRAVITY_PARTICLE.y + uniform(-1, 1) / Y_WIGGLE_SCALE))
    
    def apply_force(self, force: pygame.math.Vector2) -> None:
        self.acc += force
    
    def outside_spawn_radius(self) -> bool:
        # if the particle spawned is outside of the radius that creates the circular firework, remov it
        distance = math.sqrt((16*math.sin(self.t)**3 - self.origin.x) ** 2 + (13*math.cos(self.t) - 5*math.cos(2*self.t) - 2*math.cos(3*self.t) - math.cos(4*self.t) - self.origin.y) ** 2)
        return distance > self.explosion_radius
    
    def move(self) -> None:
        # called every frame, moves the particle
        if not self.firework:
            self.vel.x *= (X_SPREAD) * 1
            self.vel.y *= -(Y_SPREAD) * 1
            self.vel.rotate_ip(self.angle)

        if not self.stay_shape: # ADDED 
            self.vel += self.acc
            self.pos += self.vel
            self.acc *= 0
            
        elif self.stay_shape:
            self.pos += self.acc * 0.001
            self.stay_shape = False

        self.decay()

    def show(self, win: pygame.Surface) -> None:
        # draw the particle on to the surface
        x = int(self.pos.x)
        y = int(self.pos.y)
        pygame.draw.circle(win, self.colour, (x, y), self.size)

    def decay(self) -> None:
        if self.life >= self.stable_size:
            self.stay_shape = True
        
        # random decay of the particles
        if self.life > PARTICLE_LIFESPAN * 3:
            if randint(0, 15) == 0:
                self.remove = True
        # if too old, begone
        if not self.remove and self.life > PARTICLE_LIFESPAN * (1.5 + 3):
            self.remove = True
            
class CircleEmmitterParticle(object):
    def __init__(self, x, y, firework, colour, i, stable_size, radius):
        self.radius = radius
        
        self.firework = firework
        self.pos = vector2(x, y)
        self.origin = vector2(x, y)
        self.acc = vector2(0, 0)
        self.remove = False
        self.explosion_radius = randint(EXPLOSION_RADIUS_MIN, EXPLOSION_RADIUS_MAX)
        self.life = 0
        self.colour = colour
        self.t = i
        self.vel = vector2(self.radius * math.cos(self.t), self.radius * math.sin(self.t))
        self.stable_size = stable_size
        self.size = randint(PARTICLE_SIZE - 1, PARTICLE_SIZE + 1)
        self.move()
        self.outside_spawn_radius()

    def update(self) -> None:
        # called every frame
        self.life += 1
        self.move()
        self.vel = vector2(self.radius * math.cos(self.t), self.radius * math.sin(self.t))
        self.apply_force(vector2(uniform(-1, 1) / X_WIGGLE_SCALE, GRAVITY_PARTICLE.y + uniform(-1, 1) / Y_WIGGLE_SCALE))
    
    def apply_force(self, force: pygame.math.Vector2) -> None:
        self.acc += force
    
    def outside_spawn_radius(self) -> bool:
        # if the particle spawned is outside of the radius that creates the circular firework, remov it
        distance = math.sqrt((self.radius * math.cos(self.t) - self.origin.x) ** 2 + (self.radius * math.sin(self.t) - self.origin.y) ** 2)
        return distance > self.explosion_radius
    
    def move(self) -> None:
        # called every frame, moves the particle
        if not self.firework:
            self.vel.x *= (X_SPREAD) * 0.5
            self.vel.y *= (Y_SPREAD) * 0.5

            self.vel += self.acc * GRAVITY_FIREWORK.y
            self.pos += self.vel * GRAVITY_FIREWORK.y
            self.acc *= 0
        self.decay()

    def show(self, win: pygame.Surface) -> None:
        # draw the particle on to the surface
        x = int(self.pos.x)
        y = int(self.pos.y)
        pygame.draw.circle(win, self.colour, (x, y), self.size)

    def decay(self) -> None:
        if self.life >= self.stable_size:
            self.size -= 0.05
        
        # random decay of the particles
        if self.size <= 0:
            if randint(0, 15) == 0:
                self.remove = True
        # if too old, begone
        if not self.remove and self.size <= -1.5:
            self.remove = True
