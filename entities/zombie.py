import pygame
from pygame import Vector2
from utils.colors import Colors


FRAME_WIDTH = 64
FRAME_HEIGHT = 64


rot = (i + 16, 48)


class Zombie:
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.color = (0, 220, 80)
        self.hp = 10
        self.velocity = Vector2(0, 0)
        self.speed=2
        self.attack=1
        self.radius = 10
        self.frames = self.__init_dic__()
        self.direction = Vector2(0, 0)

    def draw(self, clock, screen):
        if self.is_move():
            current_frame = clock.get_time() % len(self.frames['run'])
            screen.blit(self.frames['run'][current_frame], self.position)
        else:
            current_frame = clock.get_time() % len(self.frames['idle'])
            screen.blit(self.frames['idle'][current_frame], self.position)

    def move(self, player_pos: Vector2):
        self.direction = (player_pos - self.position).normalize()
        self.position += self.direction * self.speed

    def is_move(self):
        return self.direction != Vector2(0, 0)

    def __init_dic__(self):
        sheet = pygame.image.load(r'.\pictures\ZombieToast.png')

        frames_dic = {
            'idle': [],
            'run': [],
            'jump': [],
            'die': []
        }
        step = 64 * 2
        for i in range(0, step, FRAME_WIDTH):
            frames_dic['idle'].append(sheet.subsurface((i, 0, FRAME_WIDTH, FRAME_HEIGHT)))

        start = step
        step = 6 * 64

        for i in range(start, step, FRAME_WIDTH):
            frames_dic['run'].append(sheet.subsurface((i, 0, FRAME_WIDTH, FRAME_HEIGHT)))

        start = step
        step = 14 * 64

        for i in range(start, step, FRAME_WIDTH):
            frames_dic['jump'].append(sheet.subsurface((i, 0, FRAME_WIDTH, FRAME_HEIGHT)))

        start = step
        step = 25 * 64
        for i in range(start, step, FRAME_WIDTH):
            frames_dic['die'].append(sheet.subsurface((i, 0, FRAME_WIDTH, FRAME_HEIGHT)))
        return frames_dic
