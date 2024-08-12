import numpy as np
import pygame

class ConnectFour:

    # Set number of rows and columns
    ROWS = 6
    COLUMNS = 7

    # Side length of the square that inscribes each circle
    SQUARE_RADIUS = 100

    # Radius of each circle
    CIRCLE_RADIUS = 45

    # Colour of the first player is red
    # Colour of the second player is blue
    # Colour of the frame is light brown
    # Unoccupied circles are black
    # Each tuple represents the RGB model
    FRAME = (210, 180, 140)
    UNOCCUPIED_CIRCLE = (0, 0, 0)
    FIRST_PLAYER_CIRCLE = (255, 0, 0)
    SECOND_PLAYER_CIRCLE = (0, 0, 255)

    # The width and height of the user interface
    # Note that the height has an extra row to display messages (win/lose)
    WIDTH = COLUMNS * SQUARE_RADIUS
    HEIGHT = (ROWS + 1) * SQUARE_RADIUS
    SIZE = (WIDTH, HEIGHT)

    def __init__(self):
    # Initialize Pygame
        pygame.init()
        self.user_interface = pygame.display.set_mode(self.SIZE)
        self.game_font = pygame.font.SysFont("timesnewroman", 65)

    # Create the board
    # The starting board is represented with a 2D array full of zeros
    # Player 1 circles are 1 and Player 2 circles are 2
    def create_board(self):
        self.board = np.zeros((self.ROWS, self.COLUMNS))
        return self.board

    # Add 1 or 2 to the 2D array
    def add_circle(self, row, column, added_circle):
        self.board[row][column] = added_circle

    # Test if a column is full or not
    def is_column_valid(self, col):
        return self.board[self.ROWS-1][col] == 0

    # Once we selected a column, we need to find the lowest row in which an unoccupied circle sits
    def get_row(self, column):
        for row in range(self.ROWS):
            if self.board[row][column] == 0:
                return row

    # Check if a certain move ends the game
    def check_win(self, added_circle):
        # Check horizontal wins
        for column in range(self.COLUMNS-3):
            for row in range(self.ROWS):
                if self.board[row][column] == added_circle and self.board[row][column+1] == added_circle and self.board[row][column+2] == added_circle and self.board[row][column+3] == added_circle:
                    return True

        # Check vertical wins
        for column in range(self.COLUMNS):
            for row in range(self.ROWS-3):
                if self.board[row][column] == added_circle and self.board[row+1][column] == added_circle and self.board[row+2][column] == added_circle and self.board[row+3][column] == added_circle:
                    return True

        # Check increasing diagonals
        for column in range(self.COLUMNS-3):
            for row in range(self.ROWS-3):
                if self.board[row][column] == added_circle and self.board[row+1][column+1] == added_circle and self.board[row+2][column+2] == added_circle and self.board[row+3][column+3] == added_circle:
                    return True
        
        # Check decreasing diagonals
        for column in range(self.COLUMNS-3):
            for row in range(3, self.ROWS):
                if self.board[row][column] == added_circle and self.board[row-1][column+1] == added_circle and self.board[row-2][column+2] == added_circle and self.board[row-3][column+3] == added_circle:
                    return True

    # PyGame draws and displays the board for user interface
    def display_board(self):

        # Draw the frame and unoccupied circles
        for column in range(self.COLUMNS):
            for row in range(self.ROWS):
                pygame.draw.rect(self.user_interface, self.FRAME, (column * self.SQUARE_RADIUS, row * self.SQUARE_RADIUS + self.SQUARE_RADIUS, self.SQUARE_RADIUS, self.SQUARE_RADIUS))
                pygame.draw.circle(self.user_interface, self.UNOCCUPIED_CIRCLE, (int(column * self.SQUARE_RADIUS + self.SQUARE_RADIUS/2), int(row * self.SQUARE_RADIUS + self.SQUARE_RADIUS + self.SQUARE_RADIUS/2)), self.CIRCLE_RADIUS)

        # Draw the red and blue circles depending on the situation
        for column in range(self.COLUMNS):
            for row in range(self.ROWS):
                if self.board[row][column] == 1:
                    pygame.draw.circle(self.user_interface, self.FIRST_PLAYER_CIRCLE, (int(column * self.SQUARE_RADIUS + self.SQUARE_RADIUS/2), self.HEIGHT - int(row * self.SQUARE_RADIUS + self.SQUARE_RADIUS/2)), self.CIRCLE_RADIUS)
                elif self.board[row][column] == 2:
                    pygame.draw.circle(self.user_interface, self.SECOND_PLAYER_CIRCLE, (int(column * self.SQUARE_RADIUS + self.SQUARE_RADIUS/2), self.HEIGHT - int(row * self.SQUARE_RADIUS + self.SQUARE_RADIUS/2)), self.CIRCLE_RADIUS)
        
        pygame.display.update()

    # Determines the reward of a certain action
    # reward = 1 if player wins, otherwise no reward
    def step(self, action, player):
        # action is the column
        row = self.get_row(action)
        self.add_circle(row, action, player)
        is_victorious = self.check_win(player)
        reward = 1 if is_victorious else 0
        return self.board.flatten(), reward, is_victorious
    
    # returns a list of columns that are valid
    def legal_actions(self):
        return [column for column in range(7) if self.is_column_valid(column)]
