import pygame
from pygame import Vector2
from utils.colors import Colors

FRAME_WIDTH = 64
ZOMBIE_SHIFT_X = 15
ZOMBIE_SIZE_X = 30
ZOMBIE_SHIFT_Y = 36
ZOMBIE_SIZE_Y = 28

# rot = (i + 16, 48)


class Zombie:
    def __init__(self, x, y, speed=2):
        self.position = Vector2(x, y)
        self.color = (0, 220, 80)
        self.hp = 10
        self.velocity = Vector2(0, 0)
        self.speed=speed
        self.attack=1
        self.radius = 10
        self.frames = self.__init_dic__()
        self.direction = Vector2(0, 0)
        self.cnt_die = 0
        self.cnt_running = 0
        self.die = False

    def draw_run(self, clock, screen):
        if self.is_move():
            current_frame = self.cnt_running
            self.cnt_running = (self.cnt_running + 1) % len(self.frames['run'])
            rect = self.frames['run'][current_frame].get_rect(center=self.position)
            screen.blit(self.frames['run'][current_frame], rect)
        else:
            current_frame = clock.get_time() % len(self.frames['idle'])
            rect = self.frames['idle'][current_frame].get_rect(center=self.position)
            screen.blit(self.frames['idle'][current_frame], rect)

    def draw_dying(self, screen):
        self.speed = 0
        current_frame = self.cnt_die
        self.cnt_die = (self.cnt_die + 1)
        if self.cnt_die >= 10:
            self.die = True
        self.cnt_die %= len(self.frames['die'])
        rect = self.frames['die'][current_frame].get_rect(center=self.position)
        screen.blit(self.frames['die'][current_frame], rect)

    def move(self, player_pos: Vector2):
        self.direction = (player_pos - self.position).normalize()
        self.position += self.direction * self.speed

    def is_move(self):
        return self.direction != Vector2(0, 0)

    def __init_dic__(self):
        sheet = pygame.image.load(r'.\assets\pictures\ZombieToast.png')
        print(sheet.size)
        frames_dic = {
            'idle': [],
            'run': [],
            'jump': [],
            'die': []
        }
        step = 64 * 2
        for i in range(0, step, FRAME_WIDTH):
            frames_dic['idle'].append(sheet.subsurface((i + ZOMBIE_SHIFT_X, ZOMBIE_SHIFT_Y, ZOMBIE_SIZE_X, ZOMBIE_SIZE_Y)))

        start = step
        step = 6 * 64

        for i in range(start, step, FRAME_WIDTH):
            frames_dic['run'].append(sheet.subsurface((i + ZOMBIE_SHIFT_X, ZOMBIE_SHIFT_Y, ZOMBIE_SIZE_X, ZOMBIE_SIZE_Y)))

        start = step
        step = 14 * 64

        for i in range(start, step, FRAME_WIDTH):
            frames_dic['jump'].append(sheet.subsurface((i + ZOMBIE_SHIFT_X, ZOMBIE_SHIFT_Y, ZOMBIE_SIZE_X, ZOMBIE_SIZE_Y)))

        start = step
        step = 25 * 64
        for i in range(start, step, FRAME_WIDTH):
            frames_dic['die'].append(sheet.subsurface((i + ZOMBIE_SHIFT_X, ZOMBIE_SHIFT_Y, ZOMBIE_SIZE_X, ZOMBIE_SIZE_Y)))
        return frames_dic

    def get_damage(self, bullet_pos: Vector2):
        if (bullet_pos - self.position).magnitude() < 10:
            self.hp -= 3
            return True
        return False



