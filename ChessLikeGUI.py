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
        self.POPUP_WIDTH = 600
        self.POPUP_HEIGHT = 600
        
        # Colors
        self.WHITE = (240, 240, 240)
        self.BLACK = (50, 50, 50)
        self.LIGHT_SQUARE = (245, 222, 179)
        self.DARK_SQUARE = (139, 69, 19)
        self.BLUE = (70, 130, 180)
        self.ORANGE = (255, 140, 0)
        self.HIGHLIGHT = (144, 238, 144, 128)
        self.OVERLAY = (0, 0, 0, 220)
        
        # Set up display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Transportation Chess")
        
        
        # Fonts
        self.title_font = pygame.font.Font(None, 48)
        self.info_font = pygame.font.Font(None, 32)
        self.piece_font = pygame.font.Font(None, 40)
        
        # Game state
        self.selected_square = None
        self.valid_moves = []
        self.show_rules = False

        # UI
        self.rules_button_text = self.info_font.render("Rules", True, (0, 0, 0))
        self.rules_button_rect = self.rules_button_text.get_rect(topright=(self.WINDOW_WIDTH - 10, 10))
        self.rules_lines = [
            "Goal: Capture opponent's Bike",
            "",
            "Blue goes first. Players alternate turns.",
            "",
            "Pieces:",
            " Bike (B) - Moves 1 square any direction",
            " Car (C) - Slides up to 3 squares horizontally/vertically",
            " Train (T) - Slides up to 4 squares diagonally",
            " Helicopter (H) - Jumps exactly 2 squares diagonally",
            "",
            "All pieces can move 1 square in any direction.",
            "Sliding pieces are blocked by same-color pieces.",
            "",
            "Click anywhere to close"
        ]

    def run_game(self):
        """
        The main game loop. Handles events, updates the game state, and shows the display. 
        Runs at 60fps until the user closes the window.

        :return: None
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

            if self.show_rules:
                self.draw_rules()
            
            pygame.display.flip()
            self.clock.tick(60)

        # Quits game if user kills game
        pygame.quit()
        sys.exit()

    def get_valid_moves(self, origin):
        """
        Determines which squares are valid moves for the selected piece

        :param origin: Square like "d1"

        :return: List of valid destination squares
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
        Converts column/row notation to board notation

        :param row: Row index 0-6
        :param column: Column index 0-6

        :return: Board notation like "a7"
        """
        return f"{chr(ord('a') + column)}{7 - row}"
    
    def square_to_pos(self, square):
        """
        Converts board notation to game column/row notation

        :param square: Board notation like "d4"

        :return: Tuple of (column, row)
        """
        column = ord(square[0]) - ord('a')
        row = 7 - int(square[1])
        return column, row
    
    def get_square_from_mouse(self, mouse_position):
        """
        Converts mouse click coordinates to board notation

        :param mouse_position: Tuple of (x, y) pixel coordinates

        :return: Board notation if on board, None otherwise
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
        Handles click events for all interactive elements of the game

        :param pos: Tuple of (x, y) click coordinates

        :return: None
        """
        square = self.get_square_from_mouse(pos)

        if self.rules_button_rect.collidepoint(pos) and not self.show_rules:
            self.show_rules = True
            return
        
        if self.show_rules:
            self.show_rules = False
            return

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

    def draw_board(self):
        """
        Draws the checkerboard using alternating colors, along with highlighting valid moves if a user selects
        a piece to move.

        :return: None
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

    def draw_pieces(self):
        """
        Draws the pieces on the board

        :return: None
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
        """
        Draws all the UI elements including text and rules button

        :return: None
        """
        
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

        # Draws the rules button
        pygame.draw.rect(self.screen, (200, 200, 200), self.rules_button_rect.inflate(10, 5))
        pygame.draw.rect(self.screen, (0, 0, 0), self.rules_button_rect.inflate(10, 5), 2)

        self.screen.blit(self.rules_button_text, self.rules_button_rect)
        
    def draw_rules(self):
        """
        Draws the rules popup to explain the game to users

        :return: None
        """

        # Draw transparent overlay over game window
        transparency = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), pygame.SRCALPHA)
        transparency.fill(self.OVERLAY)
        self.screen.blit(transparency, (0,0))

        x = (self.WINDOW_WIDTH - self.POPUP_WIDTH) // 2
        y = (self.WINDOW_HEIGHT - self.POPUP_HEIGHT) // 2

        popup_rect = pygame.Rect(x, y, self.POPUP_WIDTH, self.POPUP_HEIGHT)
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect)

        for line_number, line in enumerate(self.rules_lines):
            line_x = x + 20
            line_y = y + (line_number * 30) + 10

            text_surface = self.info_font.render(line, True, (0,0,0))
            self.screen.blit(text_surface, (line_x, line_y))