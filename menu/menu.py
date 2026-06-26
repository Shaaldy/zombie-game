# menu.py
import pygame
import random
from menu.settings import *


class Menu:
    """Игровое меню с фоном, кнопками и экраном настроек разрешения."""

    # ------------------------------------------------------------------
    # Инициализация
    # ------------------------------------------------------------------
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.state  = "main"          # "main" | "settings" | "confirm_quit"
        self.running = True
        self.start_game = False
        self.res_index  = 2           # индекс выбранного разрешения

        # Шрифты
        self.font_title  = pygame.font.SysFont("consolas", 64, bold=True)
        self.font_btn    = pygame.font.SysFont("consolas", 32)
        self.font_small  = pygame.font.SysFont("consolas", 22)

        # Звёздный фон — генерируем один раз
        self._gen_stars(200)

        # Анимация фона
        self._star_offset = 0.0

    # ------------------------------------------------------------------
    # Звёзды
    # ------------------------------------------------------------------
    def _gen_stars(self, n: int):
        """Создаём список (x, y, radius, speed) для параллакс-фона."""
        self.stars = [
            (
                random.randint(0, SCREEN_W),
                random.randint(0, SCREEN_H),
                random.uniform(0.5, 2.0),    # радиус
                random.uniform(0.1, 0.6),    # скорость падения
            )
            for _ in range(n)
        ]

    def _draw_bg(self, dt: float):
        """Рисуем градиент + движущиеся звёзды."""
        # --- градиент (вертикальный, построчно) ---
        for y in range(SCREEN_H):
            t = y / SCREEN_H
            r = int(COL_BG_TOP[0] + (COL_BG_BOT[0] - COL_BG_TOP[0]) * t)
            g = int(COL_BG_TOP[1] + (COL_BG_BOT[1] - COL_BG_TOP[1]) * t)
            b = int(COL_BG_TOP[2] + (COL_BG_BOT[2] - COL_BG_TOP[2]) * t)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_W, y))

        # --- звёзды ---
        self._star_offset += dt * 30          # пикселей/сек
        new_stars = []
        for x, y, rad, spd in self.stars:
            ny = (y + spd * dt * 60) % SCREEN_H
            alpha = int(180 + 75 * (rad / 2.0))
            color  = (alpha, alpha, alpha)
            pygame.draw.circle(self.screen, color, (int(x), int(ny)), int(rad))
            new_stars.append((x, ny, rad, spd))
        self.stars = new_stars

    # ------------------------------------------------------------------
    # Кнопки
    # ------------------------------------------------------------------
    def _draw_button(self, text: str, rect: pygame.Rect, hovered: bool) -> None:
        """Рисуем одну кнопку с рамкой и подсветкой при наведении."""
        color = COL_BTN_HOV if hovered else COL_BTN
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, COL_BTN_BORD, rect, width=2, border_radius=10)

        label = self.font_btn.render(text, True, COL_TEXT)
        lx = rect.centerx - label.get_width()  // 2
        ly = rect.centery - label.get_height() // 2
        self.screen.blit(label, (lx, ly))

    def _make_buttons(self, labels: list[str],
                      cx: int, start_y: int,
                      w=340, h=56, gap=20) -> list[pygame.Rect]:
        """Возвращает список Rect'ов — кнопки центрированы по cx."""
        rects = []
        for i, _ in enumerate(labels):
            r = pygame.Rect(cx - w // 2, start_y + i * (h + gap), w, h)
            rects.append(r)
        return rects

    # ------------------------------------------------------------------
    # Главный экран меню
    # ------------------------------------------------------------------
    def _handle_main(self, dt: float):
        labels = ["Новая игра", "Настройки", "Выход"]
        rects  = self._make_buttons(labels, SCREEN_W // 2, 300)
        mouse  = pygame.mouse.get_pos()

        # заголовок
        title = self.font_title.render("MY GAME", True, COL_TITLE)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 160))

        # кнопки
        for i, (label, rect) in enumerate(zip(labels, rects)):
            self._draw_button(label, rect, rect.collidepoint(mouse))

        # события
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if rects[0].collidepoint(mouse):
                    self.start_game = True
                    self.running    = False
                elif rects[1].collidepoint(mouse):
                    self.state = "settings"
                elif rects[2].collidepoint(mouse):
                    self.state = "confirm_quit"

    # ------------------------------------------------------------------
    # Экран настроек
    # ------------------------------------------------------------------
    def _handle_settings(self, dt: float):
        mouse = pygame.mouse.get_pos()

        # заголовок
        title = self.font_title.render("НАСТРОЙКИ", True, COL_TITLE)
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 120))

        # подпись
        sub = self.font_small.render("Разрешение экрана", True, COL_TEXT)
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 220))

        # --- стрелки < и > ---
        btn_w, btn_h = 50, 50
        arrow_y = 270
        r_left  = pygame.Rect(SCREEN_W // 2 - 200, arrow_y, btn_w, btn_h)
        r_right = pygame.Rect(SCREEN_W // 2 + 150, arrow_y, btn_w, btn_h)

        self._draw_button("<", r_left,  r_left.collidepoint(mouse))
        self._draw_button(">", r_right, r_right.collidepoint(mouse))

        # текущее разрешение
        rw, rh = RESOLUTIONS[self.res_index]
        res_txt = self.font_btn.render(f"{rw} × {rh}", True, COL_TEXT)
        self.screen.blit(res_txt,
                         (SCREEN_W // 2 - res_txt.get_width() // 2, arrow_y + 5))

        # кнопки Применить / Назад
        labels = ["Применить", "Назад"]
        rects  = self._make_buttons(labels, SCREEN_W // 2, 380)
        for label, rect in zip(labels, rects):
            self._draw_button(label, rect, rect.collidepoint(mouse))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if r_left.collidepoint(mouse):
                    self.res_index = (self.res_index - 1) % len(RESOLUTIONS)
                elif r_right.collidepoint(mouse):
                    self.res_index = (self.res_index + 1) % len(RESOLUTIONS)
                elif rects[0].collidepoint(mouse):    # Применить
                    pygame.display.set_mode(RESOLUTIONS[self.res_index])
                    self.screen = pygame.display.get_surface()
                    self.state  = "main"
                elif rects[1].collidepoint(mouse):    # Назад
                    self.state = "main"

    # ------------------------------------------------------------------
    # Подтверждение выхода
    # ------------------------------------------------------------------
    def _handle_confirm_quit(self, dt: float):
        mouse = pygame.mouse.get_pos()

        msg = self.font_btn.render("Выйти из игры?", True, COL_TITLE)
        self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, 280))

        labels = ["Да, выйти", "Отмена"]
        rects  = self._make_buttons(labels, SCREEN_W // 2, 360)
        for label, rect in zip(labels, rects):
            self._draw_button(label, rect, rect.collidepoint(mouse))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if rects[0].collidepoint(mouse):
                    self.running = False            # выход из программы
                elif rects[1].collidepoint(mouse):
                    self.state = "main"


    # ------------------------------------------------------------------
    # Главный цикл меню
    # ------------------------------------------------------------------
    def run(self) -> bool:
        """
        Запускает цикл меню.
        Возвращает True, если игрок нажал «Новая игра», иначе False.
        """
        clock = pygame.time.Clock()
        self.running    = True
        self.start_game = False

        while self.running:
            dt = clock.tick(60) / 1000.0      # секунды

            self._draw_bg(dt)

            if self.state == "main":
                self._handle_main(dt)
            elif self.state == "settings":
                self._handle_settings(dt)
            elif self.state == "confirm_quit":
                self._handle_confirm_quit(dt)

            pygame.display.flip()

        return self.start_game
