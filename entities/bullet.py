import pygame
from pygame.math import Vector2
from utils.colors import Colors

class Bullet:
    def __init__(self, x, y, direction):
        self.position = Vector2(x, y)                       # 64 + 64
        self.direction = direction # без нормализации         64
        self.color = (255, 215, 0)                              # 63 * 3
        self.attack = 10
        self.velocity = 100
        self.radius = 5
        self.speed = 15

    def draw(self, pygame, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def move(self):
        self.position = self.position + self.direction * self.speed
