import pygame
import sys
import random
import time

class Board:
    def __init__(self, square_width, board_width, board_height):
        self.square_width = square_width
        self.board_width = board_width
        self.board_height = board_height
        self.colors = {
            'red': (255, 0, 0),
            'yellow': (255, 255, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'black': (0, 0, 0),
        }
        self.piece_radius = square_width // 3

    def draw(self, window):
        for row in range(20):
            for column in range(4):
                square_color = self.colors['black']

                if column == 0:
                    square_color = self.colors['red']
                elif column == 1:
                    square_color = self.colors['yellow']
                elif column == 2:
                    square_color = self.colors['green']
                elif column == 3:
                    square_color = self.colors['blue']

                pygame.draw.rect(window, self.colors['black'], (column * self.square_width, row * self.square_width, self.square_width, self.square_width))
                pygame.draw.rect(window, square_color, (column * self.square_width + 1, row * self.square_width + 1, self.square_width - 2, self.square_width - 2))

class Piece:
    def __init__(self, color, column, row):
        self.color = color
        self.column = column
        self.row = row

    def move_up(self, amount):
        self.row -= amount
        if self.row < 0:
            self.row = 0

def game_main(picam, RaspberryPi = False):
    if RaspberryPi == False:
        import dice_reader_color as dc
    if RaspberryPi == True: 
        import dice_reader_color_rpi as dc
    # Initialize Pygame
    pygame.init()

    # Create the window
    square_width = 30
    board_width = 4 * square_width
    board_height = 20 * square_width
    window = pygame.display.set_mode((board_width, board_height))

    # Create the board and pieces
    board = Board(square_width, board_width, board_height)
    pieces = [Piece(board.colors['red'], 0, 19), Piece(board.colors['yellow'], 1, 19), Piece(board.colors['green'], 2, 19), Piece(board.colors['blue'], 3, 19)]

    # Main loop
    current_player = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw the board
        board.draw(window)

        # Update the position of the current player's piece each turn
        current_piece = pieces[current_player]
        players = {1: "red", 2: "yellow", 3: "green", 4: "blue"}
        print(f'It is {players[current_player + 1]} turn')
        if RaspberryPi == False:
            p, steps = dc.dice_detection(players[current_player + 1])
        if RaspberryPi == True:
            picam, steps = dc.dice_detection(players[current_player + 1], picam)  # Adjust the range according to your movement logic
        print(f'Player {players[current_player + 1]} rolled {steps}')
        current_piece.move_up(steps)  # Adjust the amount according to your movement logic

        # Check if the piece has reached the top row (victory condition)
        if current_piece.row == 0:
            print(f"Player with color {players[current_player + 1]} has won!")
            pygame.display.flip()
            pygame.time.delay(1000)
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
        pygame.time.delay(1000)  # Adjust the value to slow down the movement

        # Switch to the next player
        current_player = (current_player + 1) % len(pieces)

if __name__ == "__main__":
    picam = None
    game_main(picam, RaspberryPi =  False)
