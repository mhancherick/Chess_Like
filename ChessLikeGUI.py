# GUI for the ChessLike game built using Pygame
# Game icons sourced from flaticon.com/free-icons/

import pygame, sys
from pygame.locals import *

class ChessLikeGUI:
    """
    The GUI for the ChessLike game
    """

    def __init__(self, game):
        pygame.init()
        
        self.game = game
        self.clock = pygame.time.Clock()

        
        # Display settings
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 850
        self.BOARD_SIZE = 700
        self.SQUARE_SIZE = self.BOARD_SIZE // 7
        self.BOARD_OFFSET_X = 50
        self.BOARD_OFFSET_Y = 100
        
        # Colors
        self.WHITE = (240, 240, 240)
        self.BLACK = (50, 50, 50)
        self.LIGHT_SQUARE = (245, 222, 179)
        self.DARK_SQUARE = (139, 69, 19)
        self.BLUE = (70, 130, 180)
        self.ORANGE = (255, 140, 0)
        self.HIGHLIGHT = (144, 238, 144, 128)
        self.SELECT = (255, 255, 0, 128)
        
        # Set up display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Transportation Chess")
        icon = pygame.image.load("helicopter.png")
        pygame.display.set_icon(icon)        
        
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.info_font = pygame.font.Font(None, 32)
        self.piece_font = pygame.font.Font(None, 40)
        
        # Game state
        self.selected_square = None
        self.valid_moves = []

    def run_game(self):
        """
        The main game loop
        """

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)


                if event.type == pygame.KEYDOWN:
                    # Enables player to deselect a piece by hitting the esc key
                    if event.key == pygame.K_ESCAPE:
                        self.selected_square = None
                        self.valid_moves = []

            # Draws game screen
            self.screen.fill(self.WHITE)
            self.draw_board()
            self.draw_pieces()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)

        # Quits game if user kills game
        pygame.quit()
        sys.exit()

    def draw_board(self):
        """
        Draws the board
        """
        
        # Draw the checkerboard
        for row in range(7):
            for column in range(7):
                x = column * 100 + 50
                y = row * 100 + 75

                if (row + column) % 2 == 0:
                    color = self.WHITE
                else:
                    color = self.BLACK 

                pygame.draw.rect(self.screen, color, (x, y, 100, 100))

        # Draw board outline
        pygame.draw.rect(self.screen, (0,0,0), (50, 75, 700, 700), 1)
                

    def pos_to_square(self, column, row):
        """
        Converts Pygame column/row notation to board notation
        """
        return f"{chr(ord('a') + column)}{7 - row}"
    
    def square_to_pos(self, square):
        """
        Converts board notation to game column/row notation
        """
        column = ord(square[0]) - ord('a')
        row = 7 - int(square[1])
        return column, row
    
    def get_square_from_mouse(self, mouse_position):
        """
        
        """
        pass

    def draw_pieces(self):
        pass

    def draw_ui(self):
        pass
        

