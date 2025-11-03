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
        self.CIRCLE_RADIUS = 40
        
        # Colors
        self.WHITE = (240, 240, 240)
        self.BLACK = (50, 50, 50)
        self.LIGHT_SQUARE = (245, 222, 179)
        self.DARK_SQUARE = (139, 69, 19)
        self.BLUE = (70, 130, 180)
        self.ORANGE = (255, 140, 0)
        self.HIGHLIGHT = (144, 238, 144, 128)
        
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
        self.show_rules = False

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
        transparency = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
        transparency.fill(self.HIGHLIGHT)
        
        # Draw the checkerboard
        for row in range(7):
            for column in range(7):
                x = column * self.SQUARE_SIZE + self.BOARD_OFFSET_X
                y = row * self.SQUARE_SIZE + self.BOARD_OFFSET_Y

                if (row + column) % 2 == 0:
                    color = self.WHITE
                else:
                    color = self.BLACK 

                pygame.draw.rect(self.screen, color, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

                if self.selected_square is not None and self.square_to_pos(self.selected_square) == (column, row):
                    self.screen.blit(transparency, (x, y))

                elif self.pos_to_square(row, column) in self.valid_moves:
                    self.screen.blit(transparency, (x, y))
                    


        # Draw board outline
        pygame.draw.rect(self.screen, (0,0,0), (self.BOARD_OFFSET_X, self.BOARD_OFFSET_Y, self.BOARD_SIZE, self.BOARD_SIZE), 1)

    def get_valid_moves(self, origin):
        """
        Determines which squares are valid moves for the selected piece
        """
        valid_moves = []
        piece = self.game.get_piece(origin)
        
        if piece is None:
            return valid_moves
        

        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        rows = ['1', '2', '3', '4', '5', '6', '7']
        
        for col in columns:
            for row in rows:
                destination = col + row
                
                if destination == origin:
                    continue
                
                if self.game.check_destination(destination):
                    if piece.can_move(self.game, origin, destination):
                        valid_moves.append(destination)
        
        return valid_moves        

    def pos_to_square(self, row, column):
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
        Gets the square from the mouse position
        """
        x, y = mouse_position

        x -= self.BOARD_OFFSET_X
        y -= self.BOARD_OFFSET_Y
        x = x // self.SQUARE_SIZE
        y = y // self.SQUARE_SIZE

        if x < 0 or y < 0 or x > 6 or y > 6:
            return None
        else:
            return self.pos_to_square(y, x)





    def handle_click(self, pos):
        """
        Handles click events by selecting a piece or triggering a move
        """
        square = self.get_square_from_mouse(pos)

        if square is not None:
            if self.selected_square is None:
                piece = self.game.get_piece(square)
                if piece is not None and piece.get_color() == self.game.get_turn():
                    self.selected_square = square
                    self.valid_moves = self.get_valid_moves(square)
            else:
                self.game.make_move(self.selected_square, square)
                self.selected_square = None
                self.valid_moves = []


    

    def draw_pieces(self):
        """
        Draws the pieces on the board
        """

        for row in range(7):
            for column in range(7):
                square = self.pos_to_square(row, column)
                piece = self.game.get_piece(square)
                x = column * self.SQUARE_SIZE + self.BOARD_OFFSET_X + self.SQUARE_SIZE // 2
                y = row * self.SQUARE_SIZE + self.BOARD_OFFSET_Y + self.SQUARE_SIZE // 2

                # Draw colored circles for pieces
                if piece:
                    if piece.get_color() == "BLUE":
                        color = self.BLUE
                    else:
                        color = self.ORANGE

                    pygame.draw.circle(self.screen, color, (x, y), self.CIRCLE_RADIUS)

                    # Draw piece letters
                    text_surface = self.piece_font.render(piece.get_name()[0], True, (0,0,0))
                    text_rect = text_surface.get_rect(center=(x, y))
                    self.screen.blit(text_surface, text_rect)

    def draw_ui(self):
        
        turn = self.game.get_turn()
        game_state = self.game.get_game_state()

        color = self.BLUE if turn == "BLUE" else self.ORANGE

        if game_state == "UNFINISHED":
            title_text = self.title_font.render("Transportation Chess", True, (0,0,0))
            title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 20))
            self.screen.blit(title_text, title_rect)

            turn_text = self.info_font.render(f"{turn}'s turn", True, color)
            turn_rect = turn_text.get_rect(center=(self.WINDOW_WIDTH // 2, 60))
            self.screen.blit(turn_text, turn_rect)
        else:
            win_color = self.BLUE if game_state == "BLUE" else self.ORANGE
            title_text = self.title_font.render(f"{game_state} WON!", True, win_color)
            title_rect = title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 20))
            self.screen.blit(title_text, title_rect)
        

