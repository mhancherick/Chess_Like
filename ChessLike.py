# Description: A program that allows a user to play an transportation themed chesslike board game.
# The game takes place on a 7x7 grid with 4 different piece types, each with different movement patterns

class Piece:
    """
    Represents a piece on the ChessLike game board along with relevant attributes. Acts as the parent class of the
    specific pieces on the board (Helicopter, Train, Car, and Bike)
    """
    def __init__(self, color, direction, maximum_distance, locomotion, name):
        self._color = color
        self._direction = direction
        self._maximum_distance = maximum_distance
        self._locomotion = locomotion
        self._name = name

    def get_color(self):
        return self._color

    def get_direction(self):
        return self._direction

    def get_maximum_distance(self):
        return self._maximum_distance

    def get_locomotion(self):
        return self._locomotion

    def get_name(self):
        return self._name

    def can_move(self, game, origin, destination):
        """
        Default function that should be overridden by subclasses
        """
        raise NotImplementedError("Subclasses must implement can_move()")


class Helicopter(Piece):
    """
    Represents a Helicopter piece on the game board and holds the current position of the piece along with the attributes
    that determine legal moves. Inherits from the Piece class. Interacts with the ChessLike class.
    """
    def __init__(self, color):
        super().__init__(color, "DIAGONAL", 2, "JUMPING", "Helicopter")

    def can_move(self, game, origin, destination):
        """
        Determines if the Helicopter piece can move down the specified path given by the player
        """

        #stores origin and destination row/column identifiers in separate variables
        origin_column = origin[0]
        origin_row = int(origin[1])
        destination_column = destination[0]
        destination_row = int(destination[1])

        #calculates the distance traveled in the x and y dimensions and stores in variables
        x_delta = abs(ord(origin_column) - ord(destination_column))
        y_delta = abs(origin_row - destination_row)

        #the distance a piece moves is the maximum between the x and y deltas
        distance = max(x_delta, y_delta)

        if distance == 0:
            return False

        #if the move is not diagonal
        if x_delta != y_delta:
            #the piece can move orthogonal for a distance of one
            if distance == 1:
                return True
            #return False if an imperfect diagonal is entered by the player
            else:
                return False

        # returns false if the piece is told to move any distance other than its max distance
        if distance != self._maximum_distance:
            return False

        return True




class Train(Piece):
    """
    Represents a Train piece on the game board and holds the current position of the piece along with the attributes
    that determine legal moves. Inherits from the Piece class. Interacts with the ChessLike class.
    """

    def __init__(self, color):
        super().__init__(color, "DIAGONAL", 4, "SLIDING", "Train")

    def can_move(self, game, origin, destination):
        """
        Determines if the Train piece can move down the specified path given by the player
        """

        #stores origin and destination row/column identifiers in separate variables
        origin_column = origin[0]
        origin_row = int(origin[1])
        destination_column = destination[0]
        destination_row = int(destination[1])

        #calculates the distance traveled in the x and y dimensions and stores in variables
        x_delta = abs(ord(origin_column) - ord(destination_column))
        y_delta = abs(origin_row - destination_row)

        #the distance a piece moves is the maximum between the x and y deltas
        distance = max(x_delta, y_delta)

        if distance == 0:
            return False

        #if the move is not diagonal
        if x_delta != y_delta:
            #the piece can move orthogonal for a distance of one
            if distance == 1:
                return True
            #return False if an imperfect diagonal is entered by the player
            else:
                return False

        # returns false if the piece is told to move any distance greater than its max distance
        if distance > self._maximum_distance:
            return False

        #if locomotion is SLIDING, check every square between origin and destination
        #these variables increment, decrement or do nothing based on the movement direction
        column_direction = 0
        row_direction = 0

        if destination_column > origin_column:
            column_direction = 1
        elif destination_column < origin_column:
            column_direction = -1

        if destination_row > origin_row:
            row_direction = 1
        elif destination_row < origin_row:
            row_direction = -1

        #initializes the column and row values to be the first square that comes after the origin in the path
        column = chr(ord(origin_column) + column_direction)
        row = origin_row + row_direction

        #loop executes as long as the column or row has not reached the destination
        while column != destination_column or row != destination_row:

            #if a piece is in the path of the moving piece, return False
            if game.get_board()[f"{column}{row}"] is not None:
                return False

            #increments row and column
            column = chr(ord(column) + column_direction)
            row += row_direction

        return True


class Bike(Piece):
    """
    Represents a Bike piece on the game board and holds the current position of the piece along with the attributes
    that determine legal moves. If this piece is captured, the game is over. Inherits from the Piece class.
    Interacts with the ChessLike class.
    """

    def __init__(self, color):
        super().__init__(color, "ORTHOGONAL", 1, "JUMPING", "Bike")

    def can_move(self, game, origin, destination):
        """
        Determines if the Bike piece can move down the specified path given by the player
        """

        #stores origin and destination row/column identifiers in separate variables
        origin_column = origin[0]
        origin_row = int(origin[1])
        destination_column = destination[0]
        destination_row = int(destination[1])

        #calculates the distance traveled in the x and y dimensions and stores in variables
        x_delta = abs(ord(origin_column) - ord(destination_column))
        y_delta = abs(origin_row - destination_row)

        #the distance a piece moves is the maximum between the x and y deltas
        distance = max(x_delta, y_delta)

        #the Bike can move 1 space in any direction, so there is no path checking
        if distance != 1:
            return False
        else:
            return True
        
class Car(Piece):
    """
    Represents an Car piece on the game board and holds the current position of the piece along with the attributes
    that determine legal moves. Inherits from the Piece class. Interacts with the ChessLike class.
    """

    def __init__(self, color):
        super().__init__(color, "ORTHOGONAL", 3, "SLIDING", "Car")

    def can_move(self, game, origin, destination):
        """
        Determines if the Car piece can move down the specified path given by the player
        """

        #stores origin and destination row/column identifiers in separate variables
        origin_column = origin[0]
        origin_row = int(origin[1])
        destination_column = destination[0]
        destination_row = int(destination[1])

        #calculates the distance traveled in the x and y dimensions and stores in variables
        x_delta = abs(ord(origin_column) - ord(destination_column))
        y_delta = abs(origin_row - destination_row)

        #the distance a piece moves is the maximum between the x and y deltas
        distance = max(x_delta, y_delta)

        if distance == 0:
            return False

        #if the move is diagonal
        if x_delta == y_delta:
            #the piece can move orthogonal for a distance of one
            if distance == 1:
                return True
            #return False if a diagonal greater than 1 is entered by the player
            else:
                return False
        #return False if an imperfect diagonal is entered by the player
        elif x_delta != 0 and y_delta != 0:
            return False

        # returns false if the piece is told to move any distance greater than its max distance
        if distance > self._maximum_distance:
            return False

        #Because locomotion is SLIDING, check every square between origin and destination
        #these variables increment, decrement or do nothing based on the movement direction
        column_direction = 0
        row_direction = 0

        if destination_column > origin_column:
            column_direction = 1
        elif destination_column < origin_column:
            column_direction = -1

        if destination_row > origin_row:
            row_direction = 1
        elif destination_row < origin_row:
            row_direction = -1

        #initializes the column and row values to be the first square that comes after the origin in the path
        column = chr(ord(origin_column) + column_direction)
        row = origin_row + row_direction

        #loop executes as long as the column or row has not reached the destination
        while column != destination_column or row != destination_row:

            #if a piece is in the path of the moving piece, return False
            if game.get_board()[f"{column}{row}"] is not None:
                return False

            #increments row and column
            column = chr(ord(column) + column_direction)
            row += row_direction

        return True

class ChessLike:
    """
    Represents a game of Animal Chess. Contains current game state as well as various pieces. Manages turns, validates
    moves, and checks for wins. Utilizes the Piece subclasses for movement rules.
    """

    def __init__(self):
        self._game_state = "UNFINISHED"
        self._turn = "BLUE"

        self._board = {
            "a1":Helicopter("BLUE"),
            "b1":Train("BLUE"),
            "c1":Car("BLUE"),
            "d1":Bike("BLUE"),
            "e1":Car("BLUE"),
            "f1":Train("BLUE"),
            "g1":Helicopter("BLUE"),
            "a2":None,
            "b2": None,
            "c2": None,
            "d2": None,
            "e2": None,
            "f2": None,
            "g2": None,
            "a3": None,
            "b3": None,
            "c3": None,
            "d3": None,
            "e3": None,
            "f3": None,
            "g3": None,
            "a4": None,
            "b4": None,
            "c4": None,
            "d4": None,
            "e4": None,
            "f4": None,
            "g4": None,
            "a5": None,
            "b5": None,
            "c5": None,
            "d5": None,
            "e5": None,
            "f5": None,
            "g5": None,
            "a6": None,
            "b6": None,
            "c6": None,
            "d6": None,
            "e6": None,
            "f6": None,
            "g6": None,
            "a7": Helicopter("ORANGE"),
            "b7": Train("ORANGE"),
            "c7": Car("ORANGE"),
            "d7": Bike("ORANGE"),
            "e7": Car("ORANGE"),
            "f7": Train("ORANGE"),
            "g7": Helicopter("ORANGE"),
        }

    def get_game_state(self):
        return self._game_state

    def get_turn(self):
        return self._turn

    def get_piece(self, position):
        """
        Returns the piece at the board position if the position is valid
        """
        if position in self._board:
            return self._board[position]
        else:
            return None

    def get_board(self):
        return self._board.copy()

    def switch_turn(self):
        """
        Switches the turn to the next player
        """
        if self._turn == "ORANGE":
            self._turn = "BLUE"
        else:
            self._turn = "ORANGE"


    def make_move(self, origin, destination):
        """
        Moves the piece at the origin to the destination. Returns False if the move is invalid, otherwise returns True.
        Updates the current turn after the move has been successfully executed. Utilizes check_origin,
        check_destination, and the piece's can_move for valid move.
        Parameters: origin, destination
        Return: True if move is valid, False if move is invalid
        """

        origin = origin.lower()
        destination = destination.lower()

        if self.get_game_state() != "UNFINISHED":
            return False

        if not self.check_origin(origin):
            return False

        if not self.check_destination(destination):
            return False

        origin_piece = self._board[origin]
        if not origin_piece.can_move(self, origin, destination):
            return False

        #if the above checks pass, commit the move and switch the turn to the other player
        self.commit_move(origin, destination)

        self.switch_turn()

        return True

    def commit_move(self, origin, destination):
        """
        Makes the move specified by the player if the move is valid
        Parameters: origin, destination
        Return: none
        """

        #if the piece being captured is a Bike, end the game
        if isinstance(self._board[destination], Bike):
            self.game_over()

        #moves the piece from the origin to the destination, which removes the opposing player's piece if it
        #   is at the destination
        self._board[destination] = self._board[origin]
        self._board[origin] = None

    def check_origin(self, origin):
        """
        Checks the origin of the move to see if the entered origin is valid. Returns True if so, otherwise returns False
        Parameters: origin
        Return: True if origin is valid, False if origin is invalid
        """

        if origin not in self._board:
            return False

        piece = self._board[origin]

        #if there is not a piece at the origin, return False
        if piece is None:
            return False

        #if the piece at the origin is the wrong color, return False
        if self.get_turn() != piece.get_color():
            return False

        return True


    def check_destination(self, destination):
        """
        Checks the destination to see if the entered destination is valid. Returns True if so, otherwise returns False
        Parameters: destination
        Return: True if destination is valid, False if destination is invalid
        """

        if destination not in self._board:
            return False

        piece = self._board[destination]

        #if there isn't a piece at the destination, it's a valid destination
        if piece is None:
            return True

        #if there is a piece at the destination with the same color as the current turn, return False
        if self.get_turn() == piece.get_color():
            return False

        return True

    def game_over(self):
        """
        Prints a congratulations message and changes the game state to reflect which color won
        """
        print(f"Congratulations! {self._turn} won the game!")
        print()

        self._game_state = f"{self._turn}_WON"

    def print_board(self):
        """
        Prints the board to the console so the user can see the current state of the board
        """
        rows = ["7", "6", "5", "4", "3", "2", "1"]
        columns = ["a", "b", "c", "d", "e", "f", "g"]

        print("   " + "  ".join(columns))
        for row in rows:
            row_string = row + " "
            for column in columns:
                piece = self._board.get(column + row)
                if piece:
                    color = piece.get_color()[0]
                    animal = piece.get_name()[0]
                    row_string += color + animal + " "
                else:
                    row_string += "-- "
            print(" "+ row_string)
        print()