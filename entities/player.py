import pygame
from pygame import Vector2

from utils.colors import Colors

WIDTH = 800
HEIGHT = 800


class Player:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.frames = self.__init_frames__()
        self.color = (0, 0, 255)
        self.hp = 100
        self.velocity = Vector2(0, 0)
        self.radius = 10
        self.speed = 4
        self.cnt_running = 0

    def draw(self, screen):
        # pygame.draw.circle(screen, self.color, self.position, self.radius)

        current_frame = self.cnt_running
        self.cnt_running = (self.cnt_running + 1) % len(self.frames)
        rect = self.frames[current_frame].get_rect(center=self.position)
        screen.blit(self.frames[current_frame], rect)

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

    def __init_frames__(self):
        sheet = pygame.image.load(r'.\assets\pictures\cat.png')
        shift = 48
        fly = []
        for i in range(0, 288, shift):
            fly.append(sheet.subsurface((i, 0, shift, 64)))
        print(type(fly[0]))
        return fly

    def rotate(self):
        """
        Развернуть все анимации кошки на 180 гр.
        """
        fr = self.frames[0]

        pass



