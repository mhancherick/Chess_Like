from ChessLike import ChessLike
from ChessLikeGUI import ChessLikeGUI

# Create game instance
game = ChessLike()

# Create GUI wrapper
gui = ChessLikeGUI(game)

# Run the game
gui.run()