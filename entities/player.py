from pygame import Vector2

from utils.colors import Colors

WIDTH = 800
HEIGHT = 800


class Player:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.color = (0, 0, 255)
        self.hp = 100
        self.velocity = Vector2(0, 0)
        self.radius = 10
        self.speed = 4

    def draw(self, pygame, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def move(self, pygame, keys):
        x = self.position.x
        y = self.position.y
        if keys[pygame.K_LEFT] and x - self.radius - 1 > 0: # x
            x -= self.speed

        if keys[pygame.K_RIGHT] and x + self.radius + 1 < WIDTH:
            x += self.speed

        if keys[pygame.K_DOWN] and y + self.radius + 1 < HEIGHT:
            y += self.speed

        if keys[pygame.K_UP] and y - self.radius - 1 > 0:
            y -= self.speed

        self.position = Vector2(x, y)




