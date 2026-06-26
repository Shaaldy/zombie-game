"""
Основной модуль игры "Зомби апокалипсис"
Инициализация Pygame, создание игрового окна и главный цикл
"""

import pygame
import random

from pygame import Vector2

from entities.player import Player
from entities.zombie import Zombie
from entities.bullet import Bullet
from menu.menu import Menu
from utils.colors import Colors
from menu.settings import *

pygame.mixer.init()
pygame.mixer.music.load('assets/music/sound.mp3')


# Инициализация Pygame
pygame.init()

# Константы экрана
WIDTH = SCREEN_W
HEIGHT = SCREEN_H
FPS = 30

# Создание игрового окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Зомби апокалипсис")

#menu = Menu(screen)
#menu.run()
# Игровые объекты
clock = pygame.time.Clock()
running = True
player = Player(WIDTH // 2, HEIGHT // 2)

R = 11
bullets = []

zombies = []
for i in range(10):
    zombies.append(Zombie(random.randint(0, 789), random.randint(0, 789), random.uniform(0, 3)))

# Главный игровой цикл
while running:
    # Контроль частоты кадров
    clock.tick(FPS)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = Vector2(pygame.mouse.get_pos())
            direction = (mouse_pos - player.position).normalize()
            bullets.append(Bullet(player.position[0], player.position[1], direction))

    keys = pygame.key.get_pressed()
    player.move(pygame, keys)


    for bullet in bullets:
        hit = False
        for zombie in zombies:
            if zombie.get_damage(bullet.position):
                pygame.mixer.music.play(loops=0)
                hit = True
                break

        if hit:
            bullets.remove(bullet)
        else:
            bullet.move()
            if (bullet.position.x < 0 or bullet.position.x > WIDTH or
                    bullet.position.y < 0 or bullet.position.y > HEIGHT):
                bullets.remove(bullet)

    for zombie in zombies:
        zombie.move(player.position)

    # Очистка экрана
    screen.fill(Colors.BLACK.value)

    # Отрисовка сущностей
    player.draw(screen)
    idx = []
    for zombie in zombies:
        if zombie.die:
            zombies.remove(zombie)
        elif zombie.hp <= 0:
            zombie.draw_dying(screen)
        else:
            zombie.draw_run(clock, screen)


    for bullet in bullets:
        bullet.draw(pygame, screen)

    if len(zombies) <= 2:
        for i in range(3):
            zombies.append(Zombie(random.randint(0, 789), random.randint(0, 789), random.uniform(0, 3)))


    # Обновление экрана
    pygame.display.flip()

# Завершение работы
pygame.quit()
