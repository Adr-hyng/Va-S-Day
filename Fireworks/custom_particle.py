from modules import *
from config import *
from assets import (
    HeartEmmitterParticle,
    CircleEmmitterParticle,
    Particle
)


class HeartParticle:
    def __init__(self, position, colours, angle):
        self.position = position
        self.colours = colours
        self.angle = angle
        self.stable_size = randint(5, 10)
        self.particles = [HeartEmmitterParticle(self.position.x, self.position.y, False, choice(self.colours), i, self.angle, self.stable_size) for i in range(100)]


class SplashParticle:
    def __init__(self, position, colours):
        self.position = position
        self.colours = colours
        amount = randint(MIN_PARTICLES, MAX_PARTICLES)
        self.particles = [Particle(self.position.x, self.position.y, False, choice(self.colours)) for _ in range(amount)]

class CircleParticle:
    def __init__(self, position, colours):
        self.position = position
        self.colours = colours
        self.stable_size = randint(20, 40)
        amount = randint(MIN_PARTICLES, MAX_PARTICLES)
        self.particles = [CircleEmmitterParticle(self.position.x, self.position.y, False, choice(self.colours), i, self.stable_size, randint(10, 30)) for i in range(amount)]
