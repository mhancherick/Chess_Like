# GUI for the ChessLike game built using Pygame

import pygame, sys
from pygame.locals import *

class ChessLikeGUI:
    """
    The GUI for the ChessLike game
    """

    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((1280, 720))
        self._clock = pygame.time.Clock()

    def run_game(self):

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def create(self):
        pass

