import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, SPLIT_SPEED_MULTIPLIER
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)


    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH
        )


    def update(self, dt):
        self.position += self.velocity * dt


    def split(self):
        position = self.position
        velocity = self.velocity
        radius = self.radius

        self.kill()

        if radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        split_angle = random.uniform(20, 50)
        velocity1 = velocity.rotate(split_angle)
        velocity2 = velocity.rotate(-split_angle)

        new_radius = radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(position.x, position.y, new_radius)
        asteroid2 = Asteroid(position.x, position.y, new_radius)

        asteroid1.velocity = velocity1 * SPLIT_SPEED_MULTIPLIER
        asteroid2.velocity = velocity2 * SPLIT_SPEED_MULTIPLIER
