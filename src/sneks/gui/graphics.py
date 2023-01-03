import hashlib
import os
import struct
import sys

import pygame

from sneks.config.config import config
from sneks.gui.recorder import Recorder

ROWS = config.game.rows
COLUMNS = config.game.columns
CELL_SIZE = config.graphics.cell_size
PADDING = config.graphics.padding
COLOR_FOOD = config.graphics.colors.food
COLOR_BORDER = config.graphics.colors.border
COLOR_BACKGROUND = config.graphics.colors.background
COLOR_INVALID = config.graphics.colors.invalid

HEIGHT = (2 + ROWS) * CELL_SIZE + ROWS * PADDING
WIDTH = (2 + COLUMNS) * CELL_SIZE + COLUMNS * PADDING


class Painter:
    screen = None

    def __init__(self, recorder: Recorder = None):
        self.recorder = recorder

    def initialize(self):
        if config.graphics.headless:
            os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sneks")

    def draw_food(self, food):
        surface = pygame.Surface((CELL_SIZE - PADDING, CELL_SIZE - PADDING))
        surface.fill(COLOR_FOOD)
        rect = surface.get_rect(
            top=CELL_SIZE + PADDING + food.row * (CELL_SIZE + PADDING),
            left=CELL_SIZE + PADDING + food.column * (CELL_SIZE + PADDING),
        )
        self.screen.blit(surface, rect)

    def draw_snake(self, cells, alive, color: tuple[int, int, int]):
        surface = pygame.Surface((CELL_SIZE - PADDING, CELL_SIZE - PADDING))
        fill_horizontal = pygame.Surface((PADDING * 2, CELL_SIZE - PADDING))
        fill_vertical = pygame.Surface((CELL_SIZE - PADDING, PADDING * 2))
        surface.fill(color)
        fill_horizontal.fill(color)
        fill_vertical.fill(color)
        previous = None
        for cell in cells:
            rect = surface.get_rect(
                top=CELL_SIZE + PADDING + cell.row * (CELL_SIZE + PADDING),
                left=CELL_SIZE + PADDING + cell.column * (CELL_SIZE + PADDING),
            )
            self.screen.blit(surface, rect)
            if previous is not None:
                dr, dc = cell.row - previous.row, cell.column - previous.column
                if dr == 0:
                    if dc == -1:
                        rect = fill_horizontal.get_rect(
                            top=CELL_SIZE + cell.row * (CELL_SIZE + PADDING) + PADDING,
                            left=CELL_SIZE
                            + previous.column * (CELL_SIZE + PADDING)
                            - PADDING,
                        )
                    else:
                        rect = fill_horizontal.get_rect(
                            top=CELL_SIZE + cell.row * (CELL_SIZE + PADDING) + PADDING,
                            left=CELL_SIZE
                            + cell.column * (CELL_SIZE + PADDING)
                            - PADDING,
                        )
                    self.screen.blit(fill_horizontal, rect)
                else:
                    if dr == -1:
                        rect = fill_vertical.get_rect(
                            top=CELL_SIZE
                            + previous.row * (CELL_SIZE + PADDING)
                            - PADDING,
                            left=CELL_SIZE
                            + cell.column * (CELL_SIZE + PADDING)
                            + PADDING,
                        )
                    else:
                        rect = fill_vertical.get_rect(
                            top=CELL_SIZE + cell.row * (CELL_SIZE + PADDING) - PADDING,
                            left=CELL_SIZE
                            + cell.column * (CELL_SIZE + PADDING)
                            + PADDING,
                        )
                    self.screen.blit(fill_vertical, rect)
            previous = cell
        if not alive:
            surface.fill(COLOR_INVALID)
            rect = surface.get_rect(
                top=CELL_SIZE + PADDING + cells[0].row * (CELL_SIZE + PADDING),
                left=CELL_SIZE + PADDING + cells[0].column * (CELL_SIZE + PADDING),
            )
            self.screen.blit(surface, rect)
        else:
            surface.fill(
                struct.unpack(
                    "BBB", hashlib.md5(struct.pack("BBB", *color)).digest()[-3:]
                )
            )
            rect = surface.get_rect(
                top=CELL_SIZE + PADDING + cells[0].row * (CELL_SIZE + PADDING),
                left=CELL_SIZE + PADDING + cells[0].column * (CELL_SIZE + PADDING),
            )
            self.screen.blit(surface, rect)

    def clear(self):
        self.screen.fill(COLOR_BACKGROUND)

    def draw_boarders(self):
        top = (0, 0, WIDTH, CELL_SIZE - PADDING)
        bottom = (0, HEIGHT - CELL_SIZE + PADDING, WIDTH, HEIGHT)
        left = (0, CELL_SIZE - PADDING, CELL_SIZE - PADDING, HEIGHT)
        right = (WIDTH - CELL_SIZE + PADDING, 0, WIDTH, HEIGHT)

        for rect in (top, bottom, left, right):
            pygame.draw.rect(self.screen, COLOR_BORDER, rect)

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        if self.recorder:
            self.recorder.record_frame(self.screen)
        if not config.graphics.headless:
            pygame.time.delay(config.graphics.delay)