import pygame
import sys


# Board Class
class Board:
    # Constructor
    def __init__(self, square_width, board_width, board_height):

        self.square_width = square_width # Width of each square
        self.board_width = board_width # Width of the board
        self.board_height = board_height # Height of the board

        # Colors of the squares on the board
        self.colors = {
            'red': (255, 0, 0),
            'yellow': (255, 255, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'black': (0, 0, 0),
        }
        self.piece_radius = square_width // 3 # Radius of the player pieces

    # Draw the board
    def draw(self, window):
        # Draw the squares on the board (20 rows, 4 columns)
        for row in range(20):
            
            for column in range(4):
                # Set the color of the square to black by default
                square_color = self.colors['black']
                
                # Set the color of the square based on the column
                if column == 0:
                    square_color = self.colors['red']
                elif column == 1:
                    square_color = self.colors['yellow']
                elif column == 2:
                    square_color = self.colors['green']
                elif column == 3:
                    square_color = self.colors['blue']

                # Draw the square with a black border
                pygame.draw.rect(window, self.colors['black'], (column * self.square_width, row * self.square_width, self.square_width, self.square_width))
                pygame.draw.rect(window, square_color, (column * self.square_width + 1, row * self.square_width + 1, self.square_width - 2, self.square_width - 2))

# Piece Class
class Piece:
    # Constructor
    def __init__(self, color, column, row):

        self.color = color # Color of the piece
        self.column = column # Column of the piece
        self.row = row # Row of the piece

    # Move the piece up by the specified amount
    def move_up(self, amount):

        self.row -= amount
    
        # Make sure the piece doesn't go off the board
        if self.row < 0:
            self.row = 0

# Main function
def game_main(picam, RaspberryPi = False):
    # Import the dice reader module (depending on whether we are using the Raspberry Pi or not)
    if RaspberryPi == False:
        import dice_reader_color as dc
    if RaspberryPi == True: 
        import dice_reader_color_rpi as dc

    # Initialize Pygame
    pygame.init()

    # Create the window 
    square_width = 50
    board_width = 4 * square_width
    board_height = 20 * square_width
    window = pygame.display.set_mode((board_width, board_height))

    # Create the board 
    board = Board(square_width, board_width, board_height)

    # Create the pieces
    pieces = [Piece(board.colors['red'], 0, 19), Piece(board.colors['yellow'], 1, 19), Piece(board.colors['green'], 2, 19), Piece(board.colors['blue'], 3, 19)]

    # Dictionary to map player numbers to colors
    players = {1: "red", 2: "yellow", 3: "green", 4: "blue"}

    # Set the current player to the first player
    current_player = 0

    # Main loop 
    while True:

        # Check if the user has quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the board
        board.draw(window)

        # Update the position of the current player's piece each turn
        current_piece = pieces[current_player]
        
        # Print the current player's turn
        print(f'It is {players[current_player + 1]} turn')

        # Roll the dice and move the piece up by the specified amount (depending on whether we are using the Raspberry Pi or not)
        if RaspberryPi == False:
            p, steps = dc.dice_detection(players[current_player + 1])
        if RaspberryPi == True:
            picam, steps = dc.dice_detection(players[current_player + 1], picam)
        
        # Print the number of steps rolled
        print(f'Player {players[current_player + 1]} rolled {steps}')

        # Move the piece up by the specified amount
        current_piece.move_up(steps)  

        # Check if the piece has reached the top row (victory condition)
        if current_piece.row == 0:
            print(f"Player with color {players[current_player + 1]} has won!")
            pygame.display.flip()
            pygame.time.delay(3000)
            pygame.quit()
            sys.exit()

        # Draw all pieces in their current positions
        for piece in pieces:
            x = piece.column * square_width + square_width // 2
            y = piece.row * square_width + square_width // 2
            pygame.draw.circle(window, piece.color, (x, y), board.piece_radius)
            pygame.draw.circle(window, board.colors['black'], (x, y), board.piece_radius, 2)

        # Update the screen
        pygame.display.flip()
        pygame.time.delay(1000)

        # Switch to the next player
        current_player = (current_player + 1) % len(pieces)

# Run the game if this file is run directly without using the Raspberry Pi
if __name__ == "__main__":
    picam = None
    game_main(picam, RaspberryPi =  False)
