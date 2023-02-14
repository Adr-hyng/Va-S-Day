from modules import (
    vector2,
    choice,
    pygame,
    randint,
    uniform,
    math
)

from config import *
from assets import (
    HeartParticle,
    CircleParticle,
    SplashParticle
)

class Firework:
    def __init__(self, position: vector2, particle_type: list[str] = ["default"]):
        # self.colour = tuple(randint(0, 255) for _ in range(3))
        # self.colours = tuple(tuple(randint(0, 255) for _ in range(3)) for _ in range(3))
        self.particle_type = particle_type
        self.colour = choice([(247, 4, 36), (240, 161, 165), (251, 200, 214 ), (254, 193, 178 ) ,(254, 127, 108 )])
        self.colours = ((247, 4, 36), (240, 161, 165), (251, 200, 214 ), (254, 193, 178 ) ,(254, 127, 108 ))
        
        # Creates the firework particle
        self.firework = Particle(position.x, position.y, True, self.colour)
        self.exploded = False
        self.particles = []

    def update(self, win: pygame.Surface) -> None:
        # method called every frame
        if not self.exploded:
            self.firework.apply_force(GRAVITY_FIREWORK)
            self.firework.move()
            self.show(win)
            if self.firework.vel.y >= 0:
                self.exploded = True
                self.explode()

        else:
            for particle in self.particles:
                particle.update()
                particle.show(win)

    def explode(self):
        # when the firework has entered a stand still, create the explosion particles
        if COLORFUL:
            for p_type in self.particle_type:
                try:
                    particle_type = p_type.split("_")[0] if p_type.find("_") != -1 else p_type
                    quantity = p_type.split("_")[1] if p_type.find("_") != -1 else "1"
                    angle = (p_type.split("_")[2] if p_type.find("_") != -1 else "0")
                except Exception as e:
                    print(e)
                    quantity = 1
                    angle = 0
                    
                if "heart" == particle_type:
                    for _ in range(int(quantity)):
                        particle = HeartParticle(self.firework.pos, [(247, 4, 36), (254, 127, 108), (240, 161, 165)], int(angle))
                        
                if "default" == particle_type:
                    particle = SplashParticle(self.firework.pos, [self.colour])
                    
                if "defaultspread" == particle_type:
                    particle = SplashParticle(self.firework.pos, self.colours)
                    
                if "circle" == particle_type:
                    particle = CircleParticle(self.firework.pos, self.colours)
                    
                self.particles += particle.particles
                del particle
        else:
            self.particles = self.particle_list.get(self.particle_type).particles

    def show(self, win: pygame.Surface) -> None:
        # draw the firework on the given surface
        x = int(self.firework.pos.x)
        y = int(self.firework.pos.y)
        pygame.draw.circle(win, self.colour, (x, y), self.firework.size)

    def remove(self) -> bool:
        if not self.exploded:
            return False

        for p in self.particles:
            if p.remove:
                self.particles.remove(p)

        # remove the firework object if all particles are gone
        return len(self.particles) == 0



class Particle(object):
    def __init__(self, x, y, firework, colour):
        self.firework = firework
        self.pos = vector2(x, y)
        self.origin = vector2(x, y)
        self.acc = vector2(0, 0)
        self.remove = False
        self.explosion_radius = randint(EXPLOSION_RADIUS_MIN, EXPLOSION_RADIUS_MAX)
        self.life = 0
        self.colour = colour
        self.trail_frequency = TRAIL_FREQUENCY + randint(-3, 3)

        if self.firework:
            self.vel = vector2(0, -randint(FIREWORK_SPEED_MIN, FIREWORK_SPEED_MAX))
            self.size = FIREWORK_SIZE
        else:
            # set random position of particle 
            self.vel = vector2(uniform(-1, 1), uniform(-1, 1))
            self.vel.x *= randint(7, self.explosion_radius + 2)
            self.vel.y *= randint(7, self.explosion_radius + 2)
            self.size = randint(PARTICLE_SIZE - 1, PARTICLE_SIZE + 1)
            # update pos and remove particle if outside radius
            self.move()
            self.outside_spawn_radius()

    def update(self) -> None:
        # called every frame
        self.life += 1
        # add a new trail if life % x == 0
        if self.life % self.trail_frequency == 0:
            pass
            # trails.append(Trail(self.pos.x, self.pos.y, False, self.colour, self.size))
        # wiggle
        self.apply_force(vector2(uniform(-1, 1) / X_WIGGLE_SCALE, GRAVITY_PARTICLE.y + uniform(-1, 1) / Y_WIGGLE_SCALE))
        self.move()

    def apply_force(self, force: pygame.math.Vector2) -> None:
        self.acc += force

    def outside_spawn_radius(self) -> bool:
        # if the particle spawned is outside of the radius that creates the circular firework, remov it
        distance = math.sqrt((self.pos.x - self.origin.x) ** 2 + (self.pos.y - self.origin.y) ** 2)
        return distance > self.explosion_radius

    def move(self) -> None:
        # called every frame, moves the particle
        if not self.firework:
            self.vel.x *= X_SPREAD
            self.vel.y *= Y_SPREAD

        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        self.decay()

    def show(self, win: pygame.Surface) -> None:
        # draw the particle on to the surface
        x = int(self.pos.x)
        y = int(self.pos.y)
        pygame.draw.circle(win, self.colour, (x, y), self.size)

    def decay(self) -> None:
        # random decay of the particles
        if self.life > PARTICLE_LIFESPAN:
            if randint(0, 15) == 0:
                self.remove = True
        # if too old, begone
        if not self.remove and self.life > PARTICLE_LIFESPAN * 1.5:
            self.remove = True
