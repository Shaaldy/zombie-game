import pygame
HEIGHT = 64
WIDTH = 288

class Cat:
    def __init__(self, position):
        self.frames = self.__init_frames__()
        self.position = position

    def __init_frames__(self):
        sheet = pygame.image.load(r'.\assets\pictures\cat.png')
        shift = 48
        fly = [0] * 6
        for i in range(0, WIDTH, shift):
            fly[i] = sheet.subsurface((i, 0, i + 32, HEIGHT))
        return fly